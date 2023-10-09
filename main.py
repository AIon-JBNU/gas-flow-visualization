from pygame.locals import *
from pygame_components import *

import numpy as np
# import matplotlib.pyplot as plt
import os, sys

ethylene_folder = "/Volumes/T7/데이터 전달_KETI/Downsampling/Ethylene_500/"

data_list = {}
for i in range(1, 7):
    data_list[i] = {}
    for j in range(1, 21):
        data_list[i][j] = {}
        for heater in ['400V', '450V', '500V', '550V', '600V']:
            data_list[i][j][heater] = {}

for i in range(1, 7):
    number = 0
    for file in os.listdir(ethylene_folder + "L" + str(i)):
        file_name_split = file.split("_")

        heater = file_name_split[3]
        fan = file_name_split[6]
        if heater == "400V" and fan == "000":
            number += 1
        file_name = ethylene_folder + "L" + str(i) + "/" + file
        data_list[i][number][heater][fan] = np.load(file_name)

pygame.init()
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Test")

clock = pygame.time.Clock()
running = True

sensor_list = [] # 540 + 160 = 700
sensor_x = 300
sensor_y = 100
sensor_width = 10
sensor_height = 15
for line in range(6): # L1 ~ L6
    sensor_list.append([])
    for i in range(9): # 가로로 센서 9개
        sensor = Sensor(screen, sensor_x, sensor_y, sensor_width, sensor_height)
        for j in range(8):
            sensor.change_sensor_data(j, data_list[line + 1][14]['600V']['000'][i, :, j])
        sensor_list[line].append(sensor)
        sensor_y += sensor_height * 4 + 20
    sensor_y = 100
    sensor_x += 150

cur_time = 0

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.fill("white")

    all_end = True

    for line in range(len(sensor_list)):
        for sensor_cnt in range(len(sensor_list[line])):
            sensor = sensor_list[line][sensor_cnt]
            changed = sensor.draw(cur_time)
            if changed:
                all_end = False

    if all_end:
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(0, 0, 50, 50))

    cur_time += 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

# L1, L2, L3, L4, L5, L6
# 1~20 횟수
# 400V, 450V, 500V, 550V, 600V
# 000, 060, 100
# 라인에서의 위치(0~8), 시계열, 센서 번호(0~7)

#
# for i in range(1, 7):
#     plt.plot(data_list[i][5]['600V']['000'][4, :, 3], label='L' + str(i))
#
# plt.legend(loc='upper right')
# plt.show()
