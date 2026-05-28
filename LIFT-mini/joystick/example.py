#!/usr/bin/env python3
"""
ARX Joystick 使用示例

展示如何使用Joystick类读取手柄数据
"""

import sys
import time

# 添加joystick模块路径到Python搜索路径
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from joystick import Joystick


def main():
    # 初始化手柄，指定CAN接口名称
    # 根据你的实际CAN接口修改，如 'can0', 'can1', 'can6' 等
    can_name = 'can6'

    print(f"正在初始化手柄读取器 (CAN: {can_name})...")

    try:
        joy = Joystick(can_name)
        print("手柄初始化成功！")
        print("按 Ctrl+C 退出\n")

        while True:
            # 方法1: 获取所有轴值和按钮
            axes = joy.get_axes()
            buttons = joy.get_buttons()
            print(f"\r轴: {[f'{x:6.2f}' for x in axes]}  按钮: {buttons}", end='', flush=True)
            # 方法2: 分别获取左右摇杆
            # left_x, left_y = joy.get_left_stick()
            # right_x, right_y = joy.get_right_stick()
            # print(f"\r左摇杆: ({left_x:6.2f}, {left_y:6.2f})  "
            #       f"右摇杆: ({right_x:6.2f}, {right_y:6.2f})", end='')

            # 方法3: 获取原始数据（包括按钮）
            # raw = joy.get_raw()
            # print(f"\r原始数据: {raw}", end='')

            time.sleep(0.01)  # 100Hz 更新率

    except KeyboardInterrupt:
        print("\n\n正在退出...")
    except Exception as e:
        print(f"\n错误: {e}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
