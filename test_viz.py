#用于练习的模拟代码
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import random
import time

# 数据缓冲区，最多100个点
times = deque(maxlen=100)
values = deque(maxlen=100)

start_time = time.time()

# 初始化图表
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, 10)
ax.set_ylim(-180, 180)
ax.set_xlabel("时间 (s)")
ax.set_ylabel("角度 (deg)")
ax.set_title("实时曲线测试")

def update(frame):
    t = time.time() - start_time
    v = random.uniform(-30, 30)  # 模拟随机数据
    times.append(t)
    values.append(v)
    line.set_data(list(times), list(values))
    ax.set_xlim(max(0, t - 10), max(10, t))  # 滚动窗口
    return line,

ani = animation.FuncAnimation(fig, update, interval=50)  # 每50ms刷新
plt.show()
