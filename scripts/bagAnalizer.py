import rosbag
import argparse
import numpy as np
from bisect import bisect_left

def get_nearest(array, value):
    index0 = bisect_left(array,value)
    if index0 != len(array):
        return index0
    else:
        return -1

def adjacent_difference(array):
    return np.array([y-x for x, y in zip(array, array[1:])])

class BagImageAnalizer(object):
    def __init__(self):
        self.filename = ''
        self.topics = list()
        self.timestapms = dict()

        self.__parse_parameters()
        self.bag = None

    def initiate(self):
        try:
            self.bag = rosbag.Bag(self.filename)
        except rosbag.ROSBagException:
            print("Ошибка чтения ")
            return False
        for topic in self.topics:
            self.timestapms[topic] = list()
        for topic, msg, t in self.bag.read_messages(topics=self.topics):
            self.timestapms[topic].append(t.to_sec())
        self.bag.close()
        return True

    def get_statistics(self):
        for i in range(len(self.topics)):
            print("Статистика %d-ой камеры:"%(i + 1))
            minimum_diff, maximum_diff, mean_diff, mean_fps = self.__get_camera_statistics(self.topics[i])
            print('Минимальная разница между соседними кадрами: {:f} сек.\nМаксимальная разница между соседними кадрами: {:f} сек.\nСредняя разница между соседними кадрами: {:f} сек.\nСредний FPS: {:f} Hz\n'.format(minimum_diff, maximum_diff, mean_diff, mean_fps))
        print("Статистика стерео:")
        minimum_diff, maximum_diff, mean_diff = self.__get_stereo_statistics()
        print('Минимальная разница между кадрами камер: {:f} сек.\nМаксимальная разница между кадрами камер: {:f} сек.\nСредняя разница между кадрами камер: {:f} сек.'.format(minimum_diff, maximum_diff, mean_diff))
    def __parse_parameters(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("filename", type=str)
        parser.add_argument("--topics", nargs=2)
        args = parser.parse_args()
        self.filename = args.filename 
        self.topics = args.topics
    
    def __get_camera_statistics(self, topic):
        diffs = adjacent_difference(self.timestapms[topic])
        minimum_diff = np.min(diffs) 
        maximum_diff = np.max(diffs) 
        mean_diff = np.mean(diffs) 
        mean_fps = 1.0/mean_diff
        return minimum_diff, maximum_diff, mean_diff, mean_fps
        
    def __get_stereo_statistics(self):
        stereo_stamps = zip(self.timestapms[self.topics[0]], self.timestapms[self.topics[1]])
        stereo_diffs = np.array([np.abs(x - y) for x, y in stereo_stamps])
        minimum_diff = np.min(stereo_diffs) 
        maximum_diff = np.max(stereo_diffs) 
        mean_diff = np.mean(stereo_diffs) 
        return minimum_diff, maximum_diff, mean_diff
        

if __name__ == "__main__":
    analizer = BagImageAnalizer()
    if analizer.initiate():
        analizer.get_statistics()
