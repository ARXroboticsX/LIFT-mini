#!/bin/bash

# 调用 lift_controller 的 build.sh
cd lift_controller && ./build.sh
cd ..

# 调用 joystick 的 build.sh
cd joystick && ./build.sh
cd ..

# 在当前目录安装 Python 包
pip install -e . --break-system-packages
