import numpy as np
import math

def normalize(q:np.ndarray) ->np.ndarray:
    mag = np.linalg.norm(q)
    if mag < 1e-10:
        raise ValueError("四元数模为零，无法归一化")    
    norm = q/mag
    return norm

def multiply(q1:np.ndarray, q2:np.ndarray) ->np.ndarray:
    w  = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] -q1[3]*q2[3]
    x  = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] -q1[3]*q2[2]
    y  = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] +q1[3]*q2[1]
    z  = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] +q1[3]*q2[0]
    return np.array([w, x, y, z])

def to_dcm(q:np.ndarray) ->np.ndarray:
    q = normalize(q)
    w, x, y, z = q
    r11 = 1 - 2*(y**2 + z**2)
    r21 = 2*(x*y - w*z)
    r31 = 2*(x*z + w*y)
    r12 = 2*(x*y +w*z)
    r22 = 1-2*(x**2 + z**2)
    r32 = 2*(y*z - w*x)
    r13 = 2*(x*z -w*y)
    r23 = 2*(y*z +w*x)
    r33 = 1-2*(x**2 + y**2)
    return np.array(   [ [r11,r12,r13],
                         [r21,r22,r23],
                         [r31,r32,r33]]).T

#欧拉角顺序采用yaw -> pitch ->roll
def to_euler(q:np.ndarray) ->np.ndarray:
    q = normalize(q)
    w, x, y, z = q
    roll = math.atan2(2*(w*x+y*z), 1-2*(x**2+y**2))
    pitch = np.arcsin(np.clip(2*(w*y - z*x), -1.0, 1.0))
    yaw = math.atan2(2*(w*z +x*y),1-2*(y**2+z**2))
    return np.array([roll,pitch,yaw])

#输入必须是弧度
def from_euler(roll,pitch,yaw)->np.ndarray:
    y = yaw
    p = pitch
    r = roll
    cr = math.cos(r/2)
    sr = math.sin(r/2)
    cp = math.cos(p/2)
    sp = math.sin(p/2)
    cy = math.cos(y/2)
    sy = math.sin(y/2)
    qw = cr*cp*cy + sr*sp*sy
    qx = sr*cp*cy - cr*sp*sy
    qy = cr*sp*cy + sr*cp*sy
    qz = cr*cp*sy - sr*sp*cy

    q = np.array([qw,qx,qy,qz])
    q = normalize(q)
    return q



if __name__ == "__main__":
    q = from_euler(0, math.radians(45), math.radians(90))  
    print(to_dcm(q))  
