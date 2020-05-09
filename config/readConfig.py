"""
    封装读取config.ini文件的方法
"""
import os
import getpathinfo
import configparser


# 获取项目地址
path = getpathinfo.get_path()
# 获取config.ini文件地址
config_path =os.path.join(path, 'config', 'config.ini')
# 调用外部的读取配置文件的方法
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')


class ReadConfig(object):

    def get_https(self, name):
        value = config.get('HTTPS', name)
        return value

    def get_email(self, name):
        value = config.get('EMAIL', name)
        return value


# 调试
if __name__ == '__main__':
    print('HTTPS中的officialurl值为：', ReadConfig().get_https('online'))
    print('EMAIL中的开关on_off值为：', ReadConfig().get_email('on_off'))