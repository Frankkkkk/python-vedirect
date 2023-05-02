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
        self.parse_pdu(frames)

    def parse_pdu(self, frames):
        for frame in frames:
            if frame.startswith(b'Checksum'):
                # This entry is useless
                continue
            key, value = frame.strip().decode('utf-8').split('\t')
            self._data[key] = value


    def _get_data(self) -> list[bytes]:
        ''' Returns a PDU array, one entry per line.'''
        data = []
        with serial.Serial(self.device, self.speed, timeout=4) as s:
            # Wait for start of frame
            while True:
                frame = s.readline()
                if frame.startswith(b'PID'):
                    break

            # slurp all frames
            frame = b''
            while not frame.startswith(b'PID'):
                frame = s.readline()
                data.append(frame)


        # The checksum is for the whole DTU
        if not VEDirect.check_frame_checksum(data):
            raise InvalidChecksumException()

        return data

    @staticmethod
    def check_frame_checksum(frames: list[bytes]):
        ''' Checks the PDU for validity.
        The "checksum" generates a char so that the sum
        of all characters equals 0 mod 256'''
        chksum = 0
        for frame in frames:
            for char in frame:
                chksum = (chksum + char) % 256
        return chksum == 0



    @property
    def battery_volts(self) -> float:
        ''' Returns the battery voltage in Volts'''
        return mV(self._data['V'])

    @property
    def battery_amps(self) -> float:
        ''' Returns the battery charging current in Amps'''
        return mA(self._data['A'])

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


if __name__ == '__main__':
    v = VEDirect()
    print(f'{v.battery_volts} V')
