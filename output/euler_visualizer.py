import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time

class eulerVisualizer:
    def __init__(self, ekf, ekf_lock):
        self.ekf = ekf
        self.ekf_lock = ekf_lock
        self.times = deque(maxlen = 200)
        self.values1 = deque(maxlen = 200)
        self.values2= deque(maxlen = 200)
        self.values3 = deque(maxlen = 200)
        self.setup()
    def setup(self):
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1)
        self.line1 = self.ax1.plot([],[])[0]
        self.line2 = self.ax2.plot([],[])[0]
        self.line3 = self.ax3.plot([],[])[0]
        self.ax1.set_xlim(0,10)
        self.ax2.set_xlim(0,10)
        self.ax3.set_xlim(0,10)
        self.ax1.set_ylim(-90,90)
        self.ax2.set_ylim(-90,90)
        self.ax3.set_ylim(-90,90)
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Pitch (deg)")
        self.ax1.set_title("eulerVisualizer")
        self.ax2.set_xlabel("Time (s)")
        self.ax2.set_ylabel("Roll (deg)")
        self.ax2.set_title("eulerVisualizer")
        self.ax3.set_xlabel("Time (s)")
        self.ax3.set_ylabel("Yaw (deg)")
        self.ax3.set_title("eulerVisualizer")
        self.start_time = time.time()
        self.ax1.grid(True, alpha=0.1)
        self.ax2.grid(True, alpha=0.1)
        self.ax3.grid(True, alpha=0.1)

    def update(self,frame):
        t = time.time() - self.start_time
        self.times.append(t)
        with self.ekf_lock:
            euler = self.ekf.euler_onlyForObservation.copy()
        self.values1.append(np.degrees(euler[0]))
        self.values2.append(np.degrees(euler[1]))
        self.values3.append(np.degrees(euler[2]))
        self.line1.set_data(list(self.times),list(self.values1))
        self.line2.set_data(list(self.times),list(self.values2))
        self.line3.set_data(list(self.times),list(self.values3))
        self.ax1.set_xlim(max(0, t - 10), max(10, t))
        self.ax2.set_xlim(max(0, t - 10), max(10, t))
        self.ax3.set_xlim(max(0, t - 10), max(10, t))
        return self.line1,self.line2,self.line3
    
    def show(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=50, cache_frame_data=False)
        plt.show()


        
        

        
        
        

