#include <ros/ros.h>
#include <rosbag/bag.h>
#include <rosbag/view.h>
#include <opencv2/highgui.hpp>


class RosbagImageExtractor
{
  public:
    // RosbagImageExtractor() {}

    bool open(std::string& filename, std::string& topic);
    
    cv::Mat get_next_image();

    ~RosbagImageExtractor();
    void close();

  private:
    rosbag::View::iterator iterator_;
    std::shared_ptr<rosbag::View> view_;
    std::string topic_;
    rosbag::Bag bag_;
};
