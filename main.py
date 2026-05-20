from mserial.reader import SerialReader

def on_frame(frame):
    print(frame)

reader = SerialReader()
try:
    reader.open()
    reader.read_loop(on_frame)
except KeyboardInterrupt:
    print("\n[Main] Stopped by user")
finally:
    reader.close()
