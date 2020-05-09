"""
    获取当前项目地址
"""
import os


def get_path():

    path =os.path.split(os.path.realpath(__file__))[0]
    return path


# 调试
if __name__ == '__main__':
    print('当前文件路径：', get_path())