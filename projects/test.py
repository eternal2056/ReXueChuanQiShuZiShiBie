from numpy import *
from PIL import ImageGrab
from number_my import *
import const_my
import pyHook_test
import operation

import time
import win32api,win32gui,win32con
from ctypes import *

def clickLeftCur():
   win32api.mouse_event(
    win32con.MOUSEEVENTF_LEFTDOWN|
   win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def moveCurPos(x,y):
    windll.user32.SetCursorPos(x, y)

def click_left(x, y):
    moveCurPos(x, y)
    x1 = time.time()
    clickLeftCur()
    y1 = time.time()
    print(y1 - x1)

COLOR_LIMIT = 160
ICON = '1'
BLANK = '0'
WIDTH = 6
BORDER = 1
COLON = 2
# 获取坐标RGB [46, 176, 255]


def create_list(X1, X2, Y1, Y2, px):
    number_list = zeros((Y2 - Y1, X2 - X1), dtype=str)
    for x in range(X1, X2):
        for y in range(Y1, Y2):
            R = px[x, y][0]
            if R > COLOR_LIMIT:
                number_list[y - Y1][x - X1] = ICON
            else:
                number_list[y - Y1][x - X1] = BLANK
    return number_list


# 测试用图片
def print_test(number_list):
    for y_string in range(len(number_list)):
        print('\n', end='')
        for x_string in number_list[y_string]:
            print(x_string, end='')


# 获取冒号所在位置
def get_center(trans):
    check = 0
    for i in maohao_list:
        for j in range(4):
            if all(trans[i] == maohao1[j]) or all(trans[i] == maohao2[j]) or all(trans[i] == maohao3[j]):
                check += 1
                i += 1
        if check == 4:
            check = i - 4
            return check
        else:
            check = 0


# 获取黑边的坐标
def get_black(trans):
    check_list = []
    for i in range(len(trans)):
        if all(trans[i] == black):
            check_list.append(i)
    return check_list


# 计算出六个数字的位置
def get_number_location(center_location, black_location):
    black_all = []
    number_list_each = []
    center_add = 0
    for i in range(45):
        black_all.append(i)
    for i in range(len(black_location)):
        if len(number_list_each) == 0:
            old = black_location[i]
            number_list_each.append([])
            for j in range(0, black_location[i]):
                number_list_each[i].append(j)
            continue
        number_list_each.append([])
        if black_location[i] == old + 1:
            continue
        for j in range(old + 1, black_location[i]):
            number_list_each[i + center_add].append(j)
            if center_location == j + 1:
                center_add += 1
                number_list_each.append([])
                number_list_each.append([])
                number_list_each[i + center_add].append(center_location)
        old = black_location[i]

    number_list_each.append([])
    for j in range(old + 1, 44):
        number_list_each[i + center_add + 1].append(j)

    # print(number_list_each)
    sub = 0
    for i in range(len(number_list_each)):
        if len(number_list_each[i - sub]) <= 3:
            if len(number_list_each[i - sub]) == 1 and number_list_each[i - sub][0] == center_location:
                continue
            del number_list_each[i - sub]
            sub += 1
    return number_list_each


# 识别x轴
def get_x(rule):
    x_list = []
    for i in range(len(rule)):
        if len(rule[i]) != 1:
            x_list.append(rule[i])
        else:
            return x_list


# 识别y轴
def get_y(rule):
    y_list = rule.copy()
    for i in range(len(rule)):
        if len(rule[i]) != 1:
            del y_list[0]
        else:
            del y_list[0]
            return y_list


# 识别数字
def number_search(rule, trans):
    bit = len(rule)
    number_search_number = 0
    # 游戏显示数字
    for i in range(len(rule)): # [i] => [0,1,2,3,4,5]
        # 0~9所有数字
        right_list = []
        for number_10 in range(10):
            right = 0
            # 5列的数字 循环两次
            for number_col_5 in range(7 - len(rule[i])):
                right_temp = 0
                # 数字的列数
                for j in range(len(rule[i])):  # [i][j] => 0
                    # 数字的点数
                    for a in range(9):  # trans[rule[i][j]][a] => 1 或 0
                        if (number_10  == 0 or number_10 == 8) and (j == 1 or j == 2 or j == 3 or j == 4) and a == 4:
                            if trans[rule[i][j]][a] == number_10_list[number_10][j + number_col_5][a]:
                                right_temp += 2
                                continue
                            else:
                                right_temp -= 2
                                continue

                        # 如果两个点相同
                        if trans[rule[i][j]][a] == number_10_list[number_10][j + number_col_5][a]:
                            right_temp += 1
                        else:
                            right_temp -= 1
                if right_temp > right:
                    right = right_temp
            right_list.append(right)
        right = right_list.index(max(right_list))
        number_search_number += (10 **(bit - i - 1)) * right
    return number_search_number

def compute_other(all_people_xy, people_1):

    people_1_x = all_people_xy[0][0]
    people_1_y = all_people_xy[0][1]
    people_2_x = all_people_xy[1][0]
    people_2_y = all_people_xy[1][1]
    people_3_x = all_people_xy[2][0]
    people_3_y = all_people_xy[2][1]

    # print(const_my.people_2_list)
    people_2_x_up = (people_1_x - people_2_x) * 24 + const_my.people_2_list[0]
    people_2_y_up = (people_1_y - people_2_y) * 37

    people_3_x_up = (people_1_x - people_3_x) * 24
    people_3_y_up = (people_1_y - people_3_y) * 37 + const_my.people_3_list[1]
    # operation.operation.click_left(people_1[0], people_1[1])
    click_left(people_1[0] + people_2_x_up, people_1[1] + people_2_y_up)
    click_left(people_1[0] + people_3_x_up, people_1[1] + people_3_y_up)



# 主程序
def main(event):
    print("检测到点击事件！")
    people_1 = list(event.Position)
    if people_1[0] > 922 or people_1[1] > 524:
        return True
    all_people_xy = []
    # print(people_1)
    # 获取全屏截图
    px = ImageGrab.grab().load()
    for coordinate_i in range(len(const_my.coordinates)):
        trans = []
        center = 0
        X1 = const_my.coordinates[coordinate_i][0]
        X2 = const_my.coordinates[coordinate_i][1]
        Y1 = const_my.coordinates[coordinate_i][2]
        Y2 = const_my.coordinates[coordinate_i][3]
        number_list = create_list(X1, X2, Y1, Y2, px)
        # print_test(number_list)
        trans = transpose(number_list)
        center = get_center(trans)
        black_list = get_black(trans)
        # print(center)Q
        # print(black_list)
        number_list_each_out = get_number_location(center, black_list)
        # print(number_list_each_out)
        x_list_out = get_x(number_list_each_out)
        y_list_out = get_y(number_list_each_out)
        x_location = number_search(x_list_out, trans)
        y_location = number_search(y_list_out, trans)
        all_people_xy.append([x_location, y_location])
        # print(x_location,y_location)


    print(all_people_xy)
    compute_other(all_people_xy, people_1)
    pyHook_test.pyHook_p += 1
    return True


pyHook_test.main(main)
