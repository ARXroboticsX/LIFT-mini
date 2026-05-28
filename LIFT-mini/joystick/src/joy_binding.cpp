#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <arx_hardware_interface/ARXJoy.hpp>
#include <arx_hardware_interface/canbase/SocketCan.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <cmath>
#include <vector>

namespace py = pybind11;
using namespace arx::hw_interface;

class JoystickReader {
public:
    JoystickReader(const std::string& can_name)
        : can_name_(can_name), running_(false) {}

    ~JoystickReader() { stop(); }

    bool start() {
        if (running_) return false;

        can_.setCallBackFunction([this](CanFrame* frame) {
            joy_.read(frame);
        });
        can_.setGetMsgContentFunction([this]() {
            joy_.update();
        });

        if (!can_.Init(can_name_.c_str())) return false;

        running_ = true;
        read_thread_ = std::thread(&JoystickReader::readLoop, this);
        return true;
    }

    void stop() {
        if (running_) {
            running_ = false;
            if (read_thread_.joinable()) read_thread_.join();
        }
    }

    // 返回5个轴值: [left_y, left_x, 0.0, right_y, right_x]，范围 [-1, 1]
    std::vector<double> getAxes() {
        std::lock_guard<std::mutex> lock(mutex_);
        int raw[8];
        can_.LoadMutexMsg();
        joy_.getValue(raw);

        double f[4];
        for (int i = 0; i < 4; i++) {
            f[i] = -(double)(raw[i] - 128) / 128.0;
            if (std::abs(f[i]) < 0.04) f[i] = 0.0;
        }
        return {f[1], f[0], 0.0, f[3], f[2]};
    }

    std::vector<int> getButtons() {
        std::lock_guard<std::mutex> lock(mutex_);
        int raw[8];
        can_.LoadMutexMsg();
        joy_.getValue(raw);

        int f[4];
        for (int i = 0; i < 4; i++) {
            f[i] = raw[i + 4];
        }
        return {f[0],f[1],f[2],f[3]};
    }

    // 返回原始8个值 [axes(4) + buttons(4)]
    std::vector<int> getRaw() {
        std::lock_guard<std::mutex> lock(mutex_);
        int raw[8];
        can_.LoadMutexMsg();
        joy_.getValue(raw);
        return std::vector<int>(raw, raw + 8);
    }

private:
    void readLoop() {
        // SocketCan 内部已通过回调驱动，此线程保持存活即可
        while (running_) {
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        }
    }

    std::string can_name_;
    std::atomic<bool> running_;
    std::thread read_thread_;
    std::mutex mutex_;
    ARXJoy2026 joy_;
    SocketCan can_;
};

PYBIND11_MODULE(arx_joy_python, m) {
    m.doc() = "ARX Joystick 2026 Python bindings";

    py::class_<JoystickReader>(m, "JoystickReader")
        .def(py::init<const std::string&>(), py::arg("can_name"),
             "初始化手柄读取器\n\n参数:\n    can_name: CAN总线名称 (如 'can6')")
        .def("start", &JoystickReader::start,
             "启动CAN读取，返回是否成功")
        .def("stop", &JoystickReader::stop,
             "停止CAN读取")
        .def("get_axes", &JoystickReader::getAxes,
             "获取5个轴值 [left_y, left_x, 0.0, right_y, right_x]，范围 [-1, 1]")
        .def("get_buttons", &JoystickReader::getButtons,
             "获取按钮值")
        .def("get_raw", &JoystickReader::getRaw,
             "获取原始8个整数值 [axes(4) + buttons(4)]");
}
