#!/usr/bin/env python3
"""
ARX LIFT 2026 Python SDK 安装脚本

安装方法:
    pip install -e .    # 开发模式（推荐）
    pip uninstall arx-lift-sdk  # 卸载

安装后可以直接运行:
    python3 keyboard_control.py  # 无需 source setup.sh
"""

from setuptools import setup
import os
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))

# 检查编译产物
required_files = [
    'lift_controller/api/arx_lift_src/libarx_lift_src.so',
    'joystick/api/arx_joy/libarx_joy.so',
]

missing = [f for f in required_files if not os.path.exists(os.path.join(root_dir, f))]
if missing:
    print("\n错误: 以下文件不存在，请先编译:")
    for f in missing:
        print(f"  ✗ {f}")
    print("\n运行编译命令:")
    print("  ./build.sh")
    print()
    sys.exit(1)

setup(
    name='arx-lift-sdk',
    version='1.0.0',
    description='ARX LIFT 2026 Python SDK - 机器人控制接口',
    author='ARX Robotics',
    python_requires='>=3.6',

    # 包含的Python包
    packages=['lift_controller', 'joystick'],

    # 包含所有.so文件
    package_data={
        'lift_controller': [
            'api/arx_lift_python/*.so',
            'api/arx_lift_src/*.so',
        ],
        'joystick': [
            'api/arx_joy_python/*.so',
            'api/arx_joy/*.so',
        ],
    },

    include_package_data=True,
    zip_safe=False,
)

print("\n" + "="*60)
print("安装完成！")
print("="*60)
print("\n现在可以直接运行Python程序，无需 source setup.sh:")
print("  python3 keyboard_control.py")
print("  python3 mit_chassis_control.py")
print()
