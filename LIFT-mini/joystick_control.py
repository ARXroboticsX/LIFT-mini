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
        running_state = 1  # 运行状态固定为1
        last_time = time.time()

        print("\n手柄控制说明:")
        print("  左摇杆 Y轴: 控制升降高度")
        print("  左摇杆 X轴: 控制底盘旋转 (需要 >0.5 才生效)")
        print("  右摇杆 X轴: 控制底盘 Y 方向速度")
        print("  右摇杆 Y轴: 控制底盘 X 方向速度")
        print("\n按 Ctrl+C 退出\n")

        # 控制循环
        while True:
            # 获取手柄数据
            axes = joy.get_axes()  # [left_y, left_x, 0.0, right_y, right_x]

            # 计算时间差
            current_time = time.time()
            duration = current_time - last_time

            # 防止异常的时间跳变
            if duration > 1.0:
                duration = 0.0

            # 更新升降高度 (左摇杆Y轴)
            lift_height += axes[1] * duration / 15

            # 限制高度范围 [0, 0.39]
            if lift_height > 0.39:
                lift_height = 0.39
            elif lift_height < 0.0:
                lift_height = 0.0

            # 设置升降高度
            robot.set_height(lift_height)

            # 计算底盘旋转速度 (左摇杆X轴，需要 >0.5 才生效)
            angular_vel_z = 0.0
            if abs(axes[0]) > 0.5:
                angular_vel_z = axes[0] * 0.45

            # 设置底盘运动命令
            # axes[4]: 右摇杆X轴 -> v_y
            # axes[3]: 右摇杆Y轴 -> v_x
            robot.set_chassis_cmd(
                axes[4] / 5,      # v_x
                axes[3] / 5,      # v_y
                angular_vel_z,      # w_z
                running_state       # mode = 1
            )

            # 执行控制循环
            robot.loop()

            # 更新时间
            last_time = current_time

            print(f"\r高度: {lift_height:5.2f} | "
                f"底盘: vx={axes[3]/2.5:5.2f} vy={axes[4]/2.5:5.2f} wz={angular_vel_z:5.2f}",
                end='', flush=True)

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
