#卡尔曼观测器，用来输出姿态角
import numpy as np
from nav.quaternion import normalize, to_dcm, to_euler

class AttitudeEKF:
    def __init__(self):
        self.stateVector = np.array([1.0,0.0,0.0,0.0,0.0,0.0])
        self.P = np.eye(6) * 0.1 #协方差矩阵
        self.Q = np.eye(6) * 1e-4
        self.R = np.eye(3) * 0.1 
        self.F = np.eye(6)       #预测器状态转移雅可比
        self.K = np.zeros((6,3)) #卡尔曼增益
        self.H = np.zeros((3,6)) #观测器状态转移雅可比
        self.M = np.eye(6)
        # self.M[3, 3] = 0 #量测更新不更新YAW
        self.last_time: float | None = None
        self.euler_onlyForObservation = np.array([0.0,0.0,0.0])
    
    def predict(self, gyro:np.ndarray, dt:float):
        #状态预测方程
        w_x, w_y, w_z = np.radians(gyro)        
        real_wx = w_x - self.stateVector[4]
        real_wy = w_y - self.stateVector[5]
        real_wz = w_z
        q0 = self.stateVector[0]
        q1 = self.stateVector[1]
        q2 = self.stateVector[2]
        q3 = self.stateVector[3]
        w_bias_x = self.stateVector[4]
        w_bias_y = self.stateVector[5]
        c = dt/2
        stateVector_f1 = q0 + c*(-real_wx*q1 - real_wy*q2 - real_wz*q3)
        stateVector_f2 = q1 + c*( real_wx*q0 + real_wz*q2 - real_wy*q3)
        stateVector_f3 = q2 + c*( real_wy*q0 - real_wz*q1 + real_wx*q3)
        stateVector_f4 = q3 + c*( real_wz*q0 + real_wy*q1 - real_wx*q2)        
        stateVector_f5 = w_bias_x
        stateVector_f6 = w_bias_y
        q_after = np.array([stateVector_f1,stateVector_f2,stateVector_f3,stateVector_f4])
        q_after = normalize(q_after)
        stateVector_f1 = q_after[0]
        stateVector_f2 = q_after[1]
        stateVector_f3 = q_after[2]
        stateVector_f4 = q_after[3]
        self.stateVector =np.array([stateVector_f1,stateVector_f2,stateVector_f3,stateVector_f4,stateVector_f5,stateVector_f6])
        self.euler_onlyForObservation = to_euler(self.stateVector[0:4])

        #协方差预测方程
        self.F = np.array([[1,-c*real_wx,-c*real_wy,-c*real_wz,c*q1,c*q2],
                          [c*real_wx,1,c*real_wz,-c*real_wy,-c*q0,c*q3],
                          [c*real_wy,-c*real_wz,1,c*real_wx,-c*q3,-c*q0],
                          [c*real_wz,c*real_wy,-c*real_wx,1,c*q2,-c*q1],
                          [0,0,0,0,1,0],
                          [0,0,0,0,0,1]])
        self.P = self.F @ self.P @ self.F.T + self.Q

    #更新
    def update(self, accel:np.ndarray):
        accel_norm = accel / np.linalg.norm(accel)
        q0, q1, q2, q3,w_bias_x, w_bias_y = self.stateVector
        self.H = np.array([ [-2*q2,2*q3,-2*q0,2*q1,0,0],
                            [2*q1,2*q0,2*q3,2*q2,0,0],
                            [2*q0,-2*q1,-2*q2,2*q3,0,0]])
        S = self.H @ self.P @ self.H.T + self.R
        self.K = self.P @ self.H.T @ np.linalg.solve(S, np.eye(3))        
        measVector_f1 = 2*(q1*q3-q0*q2)
        measVector_f2 = 2*(q2*q3+q0*q1)
        measVector_f3 = 1-2*(q1**2 + q2**2)
        measVector = np.array([measVector_f1,measVector_f2,measVector_f3])
        self.stateVector = self.stateVector + self.M @ self.K @ (accel_norm - measVector )
        self.P = (np.eye(6) - self.K @ self.H) @self.P
        q = self.stateVector[0:4]
        self.stateVector[0:4] = q / np.linalg.norm(q)
        self.euler_onlyForObservation = to_euler(self.stateVector[0:4])




