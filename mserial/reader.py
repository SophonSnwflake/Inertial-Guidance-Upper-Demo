import serial
from config import SERIAL_PORT, BAUD_RATE, TIMEOUT
from mserial.parser import parse_line

class SerialReader:
    def __init__(self):
        self.ser = None

    def open(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
            print(f"[serial] 打开成功{SERIAL_PORT} @ {BAUD_RATE}")
        except serial.SerialException as e:
            print(f"[Serial] 打开失败: {e}")
            raise

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def read_loop(self, callback):
        while True:
            raw = self.ser.readline()
            if not raw:
                continue
            line = raw.decode("ascii", errors = "ignore")
            frame = parse_line(line)
            if frame is not None:
                callback(frame)
