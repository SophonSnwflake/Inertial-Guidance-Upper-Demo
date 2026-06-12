from mserial.reader import SerialReader
import numpy as np
from data.models import AGGFrame, ACCFrame, GNSSFrame
from filter.attitude import AttitudeEKF
from nav.quaternion import to_euler
from output.euler_visualizer import eulerVisualizer
import threading

ekf = AttitudeEKF()
ekf_lock = threading.Lock()
reader = SerialReader()
eulerVis = eulerVisualizer(ekf, ekf_lock)


def on_frame(frame):
    try:
        print(f"[on_frame] {frame}", flush=True)
        _on_frame_inner(frame)
    except Exception as e:
        print(f"[on_frame] 异常: {e}", flush=True)

def _on_frame_inner(frame):
    print(f"frame")
    with ekf_lock:
        if isinstance(frame,AGGFrame):
            print(f"ts={frame.timestamp}")
            gyro = np.array([frame.gx,frame.gy,frame.gz])
            if ekf.last_time is None:
                ekf.last_time = frame.timestamp / 1000
                return
            delta_time = frame.timestamp/1000 - ekf.last_time
            ekf.last_time = frame.timestamp/1000
            if delta_time <= 0 or delta_time > 0.5:
                return
            ekf.predict(gyro,delta_time)
            # print(f"[DT]predict dt={delta_time:.4f}") 
        elif isinstance(frame,ACCFrame):
            accel = np.array([frame.ax,frame.ay,frame.az])
            if ekf.last_time is None:
                ekf.last_time = frame.timestamp / 1000
                return
            ekf.update(accel)
        else:
            return
    euler = to_euler(ekf.stateVector[:4])
    print(f"roll={np.degrees(euler[0]):.4f} pitch={np.degrees(euler[1]):.4f} yaw={np.degrees(euler[2]):.4f}")

def serial_task():
    print("[Serial] 线程启动", flush=True)
    try:
        reader.open()
        print("[Serial] TCP 连接成功", flush=True)
        reader.read_loop(on_frame)
    except Exception as e:
        print(f"[Serial] 出错辣！法克鱿！ {e}", flush=True)
    finally:
        reader.close()
        print("[Serial] 线程退出", flush=True)

t_serial = threading.Thread(target=serial_task)
t_serial.daemon = True
t_serial.start()

try:
    print("[Main] 启动可视化咯！")
    eulerVis.show()
    print("[Main] plt.show() 已返回！")
except KeyboardInterrupt:
    print("\n[Main] 被用户中止")
