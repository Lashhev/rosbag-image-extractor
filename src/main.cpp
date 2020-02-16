#include "bagImageExtractor.hpp"
int main(int argc, char* argv[])
{
    RosbagImageExtractor image_extractor;
    std::string filename = "/mnt/stereo_calibr_mono.bag";
    std::string topic = "/stereo_node/left_image";
    image_extractor.open(filename, topic);
    cv::Mat image;
    do
    {
        image = image_extractor.get_next_image();
        if(!image.empty())
        {
            cv::imshow("image", image);
            cv::waitKey(1);
        }

    } while (!image.empty());
    image_extractor.close();
    return 0;
    
}