#!/usr/bin/python3

import enum
import serial

class VEDirectException(Exception):
    pass

class InvalidChecksumException(VEDirectException):
    pass

class MPPTState(enum.Enum):
    Off = 0
    Limited = 1
    Active = 2


def mA(val: str) -> float:
    return float(val) / 1000

def mV(val: str) -> float:
    return float(val) / 1000


class VEDirect:
    def __init__(self, device: str = '/dev/ttyUSB0', speed: int = 19200):
        self.device = device
        self.speed = speed
        self._data = {}

        self.refresh()


    def refresh(self):
        frames = self._get_data()

        for frame in frames:
            key, value = frame.strip().decode('utf-8').split('\t')
            self._data[key] = value


    @property
    def battery_volts(self) -> float:
        ''' Returns the battery voltage in Volts'''
        return mV(self._data['V'])

    @property
    def battery_amps(self) -> float:
        ''' Returns the battery charging current in Amps'''
        return mA(self._data['V'])

    @property
    def solar_volts(self) -> float:
        ''' Returns the solar array voltage in Volts'''
        return mV(self._data['VPV'])

    @property
    def solar_power(self) -> float:
        ''' Returns the solar array power in Watts'''
        return float(self._data['PPV'])

    @property
    def device_serial(self) -> str:
        ''' Returns the device serial number'''
        return self._data['SER#']

    @property
    def device_MPPT_state(self) -> MPPTState:
        ''' Returns the MPPT state'''
        return MPPTState(int(self._data['MPPT']))

    def _get_data(self):
        data = []
        with serial.Serial(self.device, self.speed, timeout=4) as s:
            # Wait for start of frame
            while True:
                frame = s.readline()
                if frame.startswith(b'PID'):
                    break

            data.append(frame)
            frame = s.readline()
            while not frame.startswith(b'PID'):
                data.append(frame)
                frame = s.readline()

        if not VEDirect.check_frame_checksum(data):
            raise InvalidChecksumException()

        return data

    @staticmethod
    def check_frame_checksum(frames: [bytes]):
        chksum = 0
        for char in b''.join(frames):
            chksum = (chksum + char) % 256
        return chksum == 0



v = VEDirect()
print(v.battery_volts)
