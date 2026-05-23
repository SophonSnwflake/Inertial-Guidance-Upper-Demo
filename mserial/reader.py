# import serial
# from config import SERIAL_PORT, BAUD_RATE, TIMEOUT
# from mserial.parser import parse_line
#
# class SerialReader:
#     def __init__(self):
#         self.ser = None
#
#     def open(self):
#         try:
#             self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
#             print(f"[serial] 打开成功{SERIAL_PORT} @ {BAUD_RATE}")
#         except serial.SerialException as e:
#             print(f"[Serial] 打开失败: {e}")
#             raise
#
#     def close(self):
#         if self.ser and self.ser.is_open:
#             self.ser.close()
#
#     def read_loop(self, callback):
#         while True:
#             raw = self.ser.readline()
#             if not raw:
#                 continue
#             line = raw.decode("ascii", errors = "ignore")
#             frame = parse_line(line)
#             if frame is not None:
#                 callback(frame)

import socket
from config import TCP_HOST, TCP_PORT
from mserial.parser import parse_line

class SerialReader:
    def __init__(self):
        self.sock = None
        self.buffer = ""

    def open(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #先配置好
            self.sock.connect((TCP_HOST, TCP_PORT)) #再连接
            print(f"[TCP] 连接成功 {TCP_HOST} : {TCP_PORT}")
        except Exception as e:
            print(f"[TCP] 连接失败: {e}")
            raise

    def close(self):
        if self.sock:
            self.sock.close()

    def read_loop(self, callback):
        while True:
            data = self.sock.recv(1024).decode("ascii", errors="ignore")
            if not data:
                break
            self.buffer += data
            while "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)
                frame = parse_line(line)
                if frame is not None:
                    callback(frame)        

