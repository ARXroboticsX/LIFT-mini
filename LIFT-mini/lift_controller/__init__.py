import os
import sys
import ctypes

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 预加载动态库（解决依赖问题）
lib_dir = os.path.join(current_dir, 'api', 'arx_lift_src')
lib_file = os.path.join(lib_dir, 'libarx_lift_src.so')

if os.path.exists(lib_file):
    # 使用 RTLD_GLOBAL 加载，使其符号全局可见
    ctypes.CDLL(lib_file, mode=ctypes.RTLD_GLOBAL)
else:
    raise FileNotFoundError(
        f"动态库未找到: {lib_file}\n"
        f"请先编译: cd lift_controller && ./build.sh"
    )

# 查找并导入 Python 绑定模块
def find_first_specific_so_file(root_dir, file_name):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith(file_name) and filename.endswith('.so'):
                return os.path.join(dirpath, filename)
    return None

so_file = find_first_specific_so_file(
    os.path.join(current_dir, 'api', 'arx_lift_python'),
    'arx_lift_python.'
)

if os.path.exists(so_file):
    sys.path.insert(0, os.path.dirname(so_file))
else:
    raise FileNotFoundError(
        f"Python模块未找到: {so_file}\n"
        f"请先编译: cd lift_controller && ./build.sh"
    )

# 导入主模块
from arx_lift_python import InterfacesPy, RobotType

__all__ = ['InterfacesPy', 'RobotType']
