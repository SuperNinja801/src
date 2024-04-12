import airsim
import socket
import threading
import time
import random
import queue
import pyautogui
import serial
udp_message_queue = queue.Queue()
# 连接到AirSim模拟器
client = airsim.MultirotorClient()
client.confirmConnection()

# 启动无人机引擎
client.enableApiControl(True)
client.armDisarm(True)

# 执行起飞和初始移动操作
client.takeoffAsync().join()
client.moveToZAsync(-0.2, 5).join()

# 创建UDP套接字对象并绑定端口
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("localhost", 9090))
ser = serial.Serial('com8', 115200, timeout = 0.5)  # winsows系统使用com1口连接串行口

# 是否需要恢复原速度的标志
reset_velocity = False
#速度旋转
def rotate_right(disx,disy):
    disx0=disx*0+disy*(-1)
    disy0=disx+disy*0
    return disx0,disy0
def rotate_left(disx,disy):
    disx1=disx*0+disy
    disy1=-disx+disy*0
    return disx1,disy1
# 接收UDP消息的函数
def receive_udp_messages():
    while True:
        data, address = server_socket.recvfrom(1024)
        command = data.decode('utf-8').strip()
        udp_message_queue.put(command[4])
        print(f"接收命令 from {address}: {command[4]}")
# 创建并启动线程
udp_thread = threading.Thread(target=receive_udp_messages)
udp_thread.start()
xfo=50
yfo=0
xf=50
yf=0
error_rate=0.3
#打标签c
#ue里给的udp 1是向右 0是向左 顺序是给定的
def KB_control(t):
    time.sleep(t)
    pyautogui.press('c')

def set_label_correct(ser):
    ser.write([2])
    time.sleep(0.001)
    ser.write([0])
    print('正确标签')
def set_label_error(ser):
    ser.write([1])
    time.sleep(0.001)
    ser.write([0])
    print('错误标签')

for i in range(0,25):
    threading.Thread(target=KB_control, args=(2,)).start()
    client.moveByVelocityBodyFrameAsync(3, 0, 0, 6).join()
    random_number = random.random()

    if not udp_message_queue.empty():
        str_value = udp_message_queue.get()
        print('111')
        if str_value=='1' and random_number<=error_rate:
            #错误
            print('e')
            set_label_error(ser)
            client.moveByVelocityBodyFrameAsync(0, -3, 0, 2.5).join()
        elif str_value=='1' and random_number>error_rate:
            print('c')
            set_label_correct(ser)
            client.moveByVelocityBodyFrameAsync(0, 3, 0, 2.5).join()
        if str_value == '0' and random_number <= error_rate:
            print('e')
            set_label_error(ser)
            client.moveByVelocityBodyFrameAsync(0, 3, 0, 2.5).join()
        elif str_value == '0' and random_number > error_rate:
            print('c')
            set_label_correct(ser)
            client.moveByVelocityBodyFrameAsync(0, -3, 0, 2.5).join()

client.reset()
print('结束啦！')
