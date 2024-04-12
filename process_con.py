


import airsim
import time
import random
# 连接到AirSim模拟器
client = airsim.MultirotorClient(ip='192.168.31.222')
client.confirmConnection()

# 启动无人机引擎
client.enableApiControl(True)
client.armDisarm(True)

# 起飞
client.takeoffAsync().join()

# 向前飞行
client.moveByVelocityAsync(2, 0, 0, 5).join()  # 2 m/s 的速度，持续 5 秒

# 等待一段时间
time.sleep(2)

# 向右平移
client.moveByVelocityAsync(0, -2, 0, 3).join()  # 向右平移 2 m/s，持续 3 秒

# 继续向前飞行
client.moveByVelocityAsync(2, 0, 0, 5).join()

# 最后降落
client.landAsync().join()

# 关闭无人机引擎
client.armDisarm(False)
client.enableApiControl(False)
