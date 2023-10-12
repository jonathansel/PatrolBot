#include <ros/ros.h>
#include <std_msgs/Float64.h>
#include <std_msgs/UInt8.h>
#include <geometry_msgs/TwistStamped.h>
#include <nav_msgs/Odometry.h>

#include <gazebo/common/Plugin.hh>
#include <gazebo/physics/physics.hh>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <tf2_ros/transform_broadcaster.h>


namespace gazebo {


class PatrolPlugin : public ModelPlugin {
public:
  PatrolPlugin();
  virtual ~PatrolPlugin();
  
protected:
  virtual void Load(physics::ModelPtr model, sdf::ElementPtr sdf);
  virtual void Reset();
};


GZ_REGISTER_MODEL_PLUGIN(PatrolPlugin)

}
