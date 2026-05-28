//
// Created by yezi on 2025/5/4.
//

#pragma once

#include "arx_hardware_interface/canbase/CanBaseDef.hpp"
#include <chrono>

namespace arx {
    namespace hw_interface {
        class ARXJoy {
        public:
            void read(CanFrame *frame);

            void getValue(int *button);

            void update();

        private:
            int button_[8]{0, 0, 0, 0, 0, 0, 0, 0};
            int button_buffer_[8]{0, 0, 0, 0, 0, 0, 0, 0};
        };

        class ARXJoy2026 {
        public:
            void read(CanFrame *frame);

            void getValue(int *axes_and_button);

            void update();

        private:
            int axes_and_button_[8]{0, 0, 0, 0, 0, 0, 0, 0};
            int axes_and_button_buffer_[8]{0, 0, 0, 0, 0, 0, 0, 0};
            std::chrono::system_clock::time_point last_update_time_;
        };
    } // namespace hw_interface
} // namespace arx
