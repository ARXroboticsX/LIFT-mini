#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "arx_lift_src/interfaces/InterfacesPy.hpp"

namespace py = pybind11;

PYBIND11_MODULE(arx_lift_python, m) {
    m.doc() = "ARX LIFT 2026 Python bindings";

    // 绑定 RobotType 枚举
    py::enum_<arx::InterfacesPy::RobotType>(m, "RobotType")
        .value("LIFT", arx::InterfacesPy::RobotType::LIFT)
        .value("X7S", arx::InterfacesPy::RobotType::X7S)
        .value("X72026", arx::InterfacesPy::RobotType::X72026)
        .value("LIFT2026", arx::InterfacesPy::RobotType::LIFT2026)
        .value("LIFT2026_4310_3519", arx::InterfacesPy::RobotType::LIFT2026_4310_3519)
        .export_values();

    // 绑定 InterfacesPy 类
    py::class_<arx::InterfacesPy>(m, "InterfacesPy")
        .def(py::init<const char *, arx::InterfacesPy::RobotType>(),
             py::arg("bus_name"),
             py::arg("robot_type"),
             "构造函数\n\n"
             "参数:\n"
             "    bus_name: CAN 总线名称\n"
             "    robot_type: 机器人类型")

        // Setter 方法 - 使用 Python 风格的命名
        .def("set_height", &arx::InterfacesPy::setHeight,
             py::arg("height"),
             "设置机器人高度\n\n"
             "参数:\n"
             "    height: 目标高度值")

        .def("set_waist_pos", &arx::InterfacesPy::setWaistPos,
             py::arg("pos"),
             "设置腰部位置\n\n"
             "参数:\n"
             "    pos: 目标位置值")

        .def("set_head_yaw", &arx::InterfacesPy::setHeadYaw,
             py::arg("yaw_des"),
             "设置头部偏航角\n\n"
             "参数:\n"
             "    yaw_des: 目标偏航角")

        .def("set_head_pitch", &arx::InterfacesPy::setHeadPitch,
             py::arg("pitch_des"),
             "设置头部俯仰角\n\n"
             "参数:\n"
             "    pitch_des: 目标俯仰角")

        .def("set_chassis_cmd", &arx::InterfacesPy::setChassisCmd,
             py::arg("v_x"),
             py::arg("v_y"),
             py::arg("w_z"),
             py::arg("mode"),
             "设置底盘运动命令\n\n"
             "参数:\n"
             "    v_x: X 方向速度\n"
             "    v_y: Y 方向速度\n"
             "    w_z: Z 轴角速度\n"
             "    mode: 运动模式")

        .def("set_wheel_vel", &arx::InterfacesPy::setWheelVel,
             py::arg("wheel1_vel"),
             py::arg("wheel2_vel"),
             py::arg("wheel3_vel"),
             py::arg("wheel4_vel"),
             "设置四个轮子的速度\n\n"
             "参数:\n"
             "    wheel1_vel: 轮子1速度\n"
             "    wheel2_vel: 轮子2速度\n"
             "    wheel3_vel: 轮子3速度\n"
             "    wheel4_vel: 轮子4速度")

        .def("mit_joint_control", &arx::InterfacesPy::mitJointControl,
             py::arg("id"),
             py::arg("kp"),
             py::arg("kd"),
             py::arg("pos"),
             py::arg("vel"),
             py::arg("torque"),
             "MIT 关节控制\n\n"
             "参数:\n"
             "    id: 关节ID\n"
             "    kp: 比例增益\n"
             "    kd: 微分增益\n"
             "    pos: 目标位置\n"
             "    vel: 目标速度\n"
             "    torque: 目标力矩")

        // Getter 方法 - 使用 Python 风格的命名
        .def("get_joint_state", [](arx::InterfacesPy &self, int id) {
            double pos, vel, torque;
            self.getJointState(id, pos, vel, torque);
            return py::make_tuple(pos, vel, torque);
        },
             py::arg("id"),
             "获取关节状态\n\n"
             "参数:\n"
             "    id: 关节ID\n\n"
             "返回:\n"
             "    tuple: (位置, 速度, 力矩)")

        .def("get_height", &arx::InterfacesPy::getHeight,
             "获取机器人高度\n\n"
             "返回:\n"
             "    float: 当前高度值")

        .def("get_waist_pos", &arx::InterfacesPy::getWaistPos,
             "获取腰部位置\n\n"
             "返回:\n"
             "    float: 当前腰部位置")

        .def("get_head_yaw", &arx::InterfacesPy::getHeadYaw,
             "获取头部偏航角\n\n"
             "返回:\n"
             "    float: 当前偏航角")

        .def("get_head_pitch", &arx::InterfacesPy::getHeadPitch,
             "获取头部俯仰角\n\n"
             "返回:\n"
             "    float: 当前俯仰角")

        .def("get_wheel_vel", [](arx::InterfacesPy &self) {
            double vel[4];
            self.getWheelVel(vel);
            return py::array_t<double>(4, vel);
        },

             "获取四个轮子的速度\n\n"
             "返回:\n"
             "    numpy.ndarray: 包含4个轮子速度的数组")
        .def("get_wheel_des_vel", [](arx::InterfacesPy &self) {
            double vel[4];
            self.getWheelDesireVel(vel);
            return py::array_t<double>(4, vel);
        },
             "获取四个轮子的期望速度\n\n"
             "返回:\n"
             "    numpy.ndarray: 包含4个轮子期望速度的数组")
        .def("get_orientation", [](arx::InterfacesPy &self) {
            double orientation[3];
            self.getOrientation(orientation);
            return py::array_t<double>(3, orientation);
        },
             "获取机器人姿态\n\n"
             "返回:\n"
             "    numpy.ndarray: 包含姿态信息的数组 [roll, pitch, yaw]")

        .def("get_angular_vel", [](arx::InterfacesPy &self) {
            double angular_vel[3];
            self.getAngularVel(angular_vel);
            return py::array_t<double>(3, angular_vel);
        },
             "获取角速度\n\n"
             "返回:\n"
             "    numpy.ndarray: 包含角速度信息的数组 [wx, wy, wz]")

        .def("get_accel", [](arx::InterfacesPy &self) {
            double accel[3];
            self.getAccel(accel);
            return py::array_t<double>(3, accel);
        },
             "获取加速度\n\n"
             "返回:\n"
             "    numpy.ndarray: 包含加速度信息的数组 [ax, ay, az]")

        // 其他方法
        .def("loop", &arx::InterfacesPy::loop,
             "执行控制循环")

        .def("protect", &arx::InterfacesPy::protect,
             "执行保护逻辑");
}