"""
ARX Joystick 2026 Python API
提供手柄数据读取的高级接口
"""

import os
import sys
import ctypes
import time
from typing import List, Tuple

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 预加载动态库（解决依赖问题）
lib_dir = os.path.join(current_dir, 'api', 'arx_joy')
lib_file = os.path.join(lib_dir, 'libarx_joy.so')

if os.path.exists(lib_file):
    # 使用 RTLD_GLOBAL 加载，使其符号全局可见
    ctypes.CDLL(lib_file, mode=ctypes.RTLD_GLOBAL)
else:
    raise FileNotFoundError(
        f"动态库未找到: {lib_file}\n"
        f"请先编译: cd joystick && ./build.sh"
    )

# 查找并导入 Python 绑定模块
def find_first_specific_so_file(root_dir, file_name):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith(file_name) and filename.endswith('.so'):
                return os.path.join(dirpath, filename)
    return None

so_file = find_first_specific_so_file(
    os.path.join(current_dir, 'api', 'arx_joy_python'),
    'arx_joy_python.'
)

if os.path.exists(so_file):
    sys.path.insert(0, os.path.dirname(so_file))
    from arx_joy_python import JoystickReader as _JoystickReader
else:
    raise FileNotFoundError(
        f"Python模块未找到: {so_file}\n"
        f"请先编译: cd joystick && ./build.sh"
    )


class Joystick:
    """
    ARX手柄读取器

    自动在后台线程读取CAN帧，提供简单的接口获取手柄状态

    参数:
        can_name: CAN总线名称，如 'can6'

    示例:
        >>> from joystick import Joystick
        >>> joy = Joystick('can6')
        >>> axes = joy.get_axes()
        >>> print(f"左摇杆: ({axes[1]:.2f}, {axes[0]:.2f})")
    """

    def __init__(self, can_name: str):
        self._reader = _JoystickReader(can_name)
        self._started = False

        if not self._reader.start():
            raise RuntimeError(f"无法初始化CAN接口: {can_name}")

        self._started = True
        time.sleep(0.1)  # 等待数据稳定

    def __del__(self):
        """析构时停止读取"""
        self.stop()

    def stop(self):
        """停止CAN读取"""
        if self._started:
            self._reader.stop()
            self._started = False

    def get_axes(self) -> List[float]:
        """
        获取手柄摇杆值

        返回:
            [left_y, left_x, 0.0, right_y, right_x]
            范围: [-1.0, 1.0]，死区已处理
        """
        if not self._started:
            raise RuntimeError("手柄读取器未启动")
        return self._reader.get_axes()
    
    def get_buttons(self) -> List[int]:
        if not self._started:
            raise RuntimeError("手柄读取器未启动")
        return self._reader.get_buttons()

    def get_left_stick(self) -> Tuple[float, float]:
        """获取左摇杆 (x, y)"""
        axes = self.get_axes()
        return (axes[1], axes[0])

    def get_right_stick(self) -> Tuple[float, float]:
        """获取右摇杆 (x, y)"""
        axes = self.get_axes()
        return (axes[4], axes[3])

    def get_raw(self) -> List[int]:
        """获取原始数据（8个整数）"""
        if not self._started:
            raise RuntimeError("手柄读取器未启动")
        return self._reader.get_raw()


__all__ = ['Joystick']
