#!/usr/bin/env python3
"""
ARX LIFT 2026 手柄控制程序

使用手柄控制机器人的升降和底盘运动
"""

import time
from lift_controller import InterfacesPy, RobotType
from joystick import Joystick


def main():
    # 配置
    CAN_ROBOT = 'can5'  # 机器人CAN接口
    CAN_JOYSTICK = 'can6'  # 手柄CAN接口
    ROBOT_TYPE = RobotType.LIFT2026_4310_3519

    print("正在初始化机器人和手柄...")

    try:
        # 初始化机器人
        robot = InterfacesPy(CAN_ROBOT, ROBOT_TYPE)
        print(f"✓ 机器人已连接 (CAN: {CAN_ROBOT})")

        # 初始化手柄
        joy = Joystick(CAN_JOYSTICK)
        print(f"✓ 手柄已连接 (CAN: {CAN_JOYSTICK})")

        # 控制参数
        robot.loop()
        lift_height = robot.get_height()  # 当前升降高度
        last_time = time.time()


        # 控制循环
        while True:

            # 设置升降高度  (0,0.38)!!!!!!!
            # 此处为了保持上电后无需复位，设置增量值
            # set_height_cmd=0     #距启动前，增加的高度值
            # set_lift_height=lift_height+set_height_cmd
            # robot.set_height(set_lift_height)


            # 设置底盘速度 x y z mode =1 为整体速度控制  单位m/s
            # robot.set_chassis_cmd(0,0,0,1)

            
            # 轮速控制，设置模式为3
            # robot.set_chassis_cmd(0,0,0,3)
            # robot.set_wheel_vel(1,0,0,0)


            # 获取高度值
            get_chassis_height=robot.get_height()

            # 轮速获取
            get_wheel_vel=robot.get_wheel_vel()

            print(f"当前高度: {get_chassis_height}")
            print(f"轮速: {get_wheel_vel}")






            # 执行控制循环
            robot.loop()
            time.sleep(0.0025)

    except KeyboardInterrupt:
        print("\n\n正在退出...")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
