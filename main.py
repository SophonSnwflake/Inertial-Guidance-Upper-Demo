from mserial.reader import SerialReader
import numpy as np
from data.models import AGGFrame, ACCFrame, GNSSFrame
from filter.attitude import AttitudeEKF
from nav.quaternion import to_euler

ekf = AttitudeEKF()
reader = SerialReader()


def on_frame(frame):
#     print(frame)
    if isinstance(frame,AGGFrame):
        gyro = np.array([frame.gx,frame.gy,frame.gz])
        if ekf.last_time is None:
            ekf.last_time = frame.timestamp / 1000
            return
        delta_time = frame.timestamp/1000 - ekf.last_time
        ekf.last_time = frame.timestamp/1000
        if delta_time <= 0 or delta_time > 0.5:
            return        
        ekf.predict(gyro,delta_time)
    elif isinstance(frame,ACCFrame):
        accel = np.array([frame.ax,frame.ay,frame.az])
        if ekf.last_time is None:
            ekf.last_time = frame.timestamp / 1000
            return
        ekf.update(accel)
    euler = to_euler(ekf.stateVector[:4])
    print(f"roll={np.degrees(euler[0]):.4f} pitch={np.degrees(euler[1]):.4f} yaw={np.degrees(euler[2]):.4f}")

try:
    reader.open()
    reader.read_loop(on_frame)
except KeyboardInterrupt:
    print("\n[Main] Stopped by user")
finally:
    reader.close()
