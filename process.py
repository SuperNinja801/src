import time
import airsim
import random
# import serial
def draw(client,i,dir):
    kinematics_state = client.simGetGroundTruthKinematics()
    position = kinematics_state.position
    label=random.random()
    if label < 0.3:
        flag=dir[i]
    else:
        flag=-dir[i]
    #1是箭头指向下 -1是箭头向下

    start = airsim.Vector3r(position.x_val+8, position.y_val, position.z_val)
    direction = airsim.Vector3r(position.x_val+8, position.y_val, position.z_val+2*flag)
    client.simPlotArrows([start],
                         [direction],
                         color_rgba=[1.0, 0.0, 0.0, 1.0], duration=0.5, arrow_size=150, thickness=10)
    return label
def draw_mode2(client,i,dir):
    kinematics_state = client.simGetGroundTruthKinematics()
    position = kinematics_state.position
    flag=dir[i]
    start = airsim.Vector3r(position.x_val + 8, position.y_val, position.z_val)
    direction = airsim.Vector3r(position.x_val + 8, position.y_val, position.z_val + 2 * flag)
    client.simPlotArrows([start],
                         [direction],
                         color_rgba=[0.0, 1.0, 0.0, 1.0], duration=0.5, arrow_size=150, thickness=10)
    return direction
if __name__ == '__main__':

    n=input('select mode')
    # ser = serial.Serial('com8', 115200, timeout = 0.5)  # winsows系统使用com1口连接串行口
    #实例化serial
    # 连接到AirSim
    client = airsim.MultirotorClient(ip='172.20.10.14')
    client.reset()
    client.confirmConnection()
    # 获取无人机初始状态
    state = client.getMultirotorState()
    position = state.kinematics_estimated.position
    orientation = state.kinematics_estimated.orientation
    client.enableApiControl(True)
    client.armDisarm(True)
    client.moveToZAsync(-40, 15).join()
    time.sleep(3)
    dir=[1,-1,-1,1,-1,1,-1,1,-1,1,1,-1,1,1,-1,-1,-1,1,1,-1,1,-1,-1,1,-1,1,-1,1,-1,1,1,-1,1,1,-1,-1,-1,1,1,-1,-1,1,1,-1,1,-1,-1,1,-1,1]
    #1是向上飞 -1是向下飞
    for i in range(0,50):
        kinematics_state = client.simGetGroundTruthKinematics()
        position = kinematics_state.position
        label=draw(client,i,dir)
        time.sleep(1)
        #打标签
        # print(label)
        # ser.write([0])
        # time.sleep(0.001)
        # if label<0.3:
        #     ser.write([1])
        #     time.sleep(0.001)
        #     ser.write([0])
        # else:
        #     ser.write([2])
        #     time.sleep(0.001)
        #     ser.write([0])
        nextHight=position.z_val-dir[i]*10
        if n==1:
            client.moveToZAsync(nextHight,10).join()
        else:
            time.sleep(1.5)
            draw_mode2(client,i,dir)

        time.sleep(3)
    client.reset()

