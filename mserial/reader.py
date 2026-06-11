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
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(3.0)
            self.sock.connect((TCP_HOST, TCP_PORT))
            self.sock.settimeout(1.0)
            print(f"[TCP] 连接成功 {TCP_HOST} : {TCP_PORT}")
        except Exception as e:
            print(f"[TCP] 连接失败: {e}")
            raise

    def close(self):
        if self.sock:
            self.sock.close()

    def read_loop(self, callback):
        while True:
            try:
                data = self.sock.recv(1024).decode("ascii", errors="ignore")
            except TimeoutError:
                print("[TCP] 等待数据...", flush=True)
                continue
            if not data:
                print("[TCP] 连接已断开")
                break
            # print(f"[TCP] 收到 {len(data)} 字节: {repr(data[:80])}", flush=True)
            self.buffer += data
            while "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)
                frame = parse_line(line)
                if frame is not None:
                    callback(frame)

