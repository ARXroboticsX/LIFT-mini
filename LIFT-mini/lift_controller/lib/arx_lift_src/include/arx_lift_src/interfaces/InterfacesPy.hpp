#pragma once

#include <memory>
#include <string>
#include <vector>

namespace arx {

class InterfacesPy {
 public:
  enum class RobotType {
    LIFT,
    X7S,
    X72026,
    LIFT2026,
    LIFT2026_4310_3519,
    LIFT2026_4310_80,
  };

  InterfacesPy(const char *bus_name, RobotType robot_type);
  ~InterfacesPy();

  void setHeight(double height);
  void setWaistPos(double pos);
  void setHeadYaw(double yaw_des);
  void setHeadPitch(double pitch_des);
  void setChassisCmd(double v_x, double v_y, double w_z, int mode);
  void setWheelVel(double wheel1_vel, double wheel2_vel, double wheel3_vel, double wheel4_vel);
  void mitJointControl(int id, double kp, double kd, double pos, double vel, double torque);
  void getJointState(int id, double &pos, double &vel, double &torque);

  double getHeight();
  double getWaistPos();
  double getHeadYaw();
  double getHeadPitch();
  void getWheelVel(double *vel);
  void getWheelDesireVel(double *vel);
  void getOrientation(double *orientation);
  void getAngularVel(double *angular_vel);
  void getAccel(double *accel);

  void loop();
  void protect();

 private:
  class impl;
  std::unique_ptr<impl> pimpl;
};

}// namespace arx