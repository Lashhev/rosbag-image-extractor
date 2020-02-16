#include "bagImageExtractor.hpp"
#include <sensor_msgs/Image.h>
#include <cv_bridge/cv_bridge.h>

bool RosbagImageExtractor::open(std::string &filename, std::string& topic)
{
    topic_ = topic;
    try
    {
        bag_.open(filename, rosbag::BagMode::Read);
    }
    catch(const rosbag::BagException& e)
    {
        ROS_ERROR("Enable to open bag file \'%s\'", filename.c_str());
        std::cerr << e.what() << '\n';
        return false;
    }

    view_ = std::make_shared<rosbag::View>(bag_, rosbag::TopicQuery(topic_));

    iterator_ = (*(view_.get())).begin();
    if(iterator_ == (*(view_.get())).end())
    return false;
}

RosbagImageExtractor::~RosbagImageExtractor()
{
    close();
}

cv::Mat RosbagImageExtractor::get_next_image()
{
    cv::Mat cv_image;
    if(iterator_ != (*(view_.get())).end())
    {
        sensor_msgs::Image::ConstPtr image = iterator_->instantiate<sensor_msgs::Image>();
        cv_bridge::CvImagePtr cv_ptr;
        try
        {
            cv_ptr = cv_bridge::toCvCopy(image, sensor_msgs::image_encodings::MONO8);
        }
        catch (cv_bridge::Exception& e)
        {
            ROS_ERROR("cv_bridge exception: %s", e.what());
        }
        cv_ptr->image.copyTo(cv_image);
        iterator_++;
    }
    return cv_image;
}

void RosbagImageExtractor::close() 
{
    if(bag_.isOpen())
        bag_.close();
}