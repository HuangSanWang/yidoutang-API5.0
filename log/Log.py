"""
    封装log方法，并输入log到指定文件
"""
import os
import getpathinfo
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime


# 获取项目地址
path = getpathinfo.get_path()
# 存放log文件的路径
log_path =os.path.join(path, 'result')


class Logger(object):
    # 内置参数
    def __init__(self, logger_name='logs'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        self.today = str(datetime.date.today())
        # 日志文件名称
        self.log_file_name = 'logs' + self.today
        # 最多存放日志的数量
        self.backup_count = 5
        # 控制台日志输出级别
        self.console_output_level = 'WARNING'
        # log文件输出级别
        self.file_output_level = 'DEBUG'
        # 日志输出格式
        """        
            %(levelno)s：打印日志级别的数值
            %(levelname)s：打印日志级别的名称
            %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
            %(filename)s：打印当前执行程序名
            %(funcName)s：打印日志的当前函数
            %(lineno)d：打印日志的当前行号
            %(asctime)s：打印日志的时间
            %(thread)d：打印线程ID
            %(threadName)s：打印线程名称
            %(process)d：打印进程ID
            %(message)s：打印日志信息
            %(name)s:打印日志名称
        """
        self.formatter = logging.Formatter('[%(asctime)s - %(name)s] - %(filename)s - %(levelname)s - %(message)s')

    def get_logger(self):
        """
            在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
        """
        if not self.logger.handlers: # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=os.path.join(log_path, self.log_file_name), when='D',
                                                    interval=1, backupCount=self.backup_count, delay=True,
                                                    encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Logger().get_logger()


# 调试
if __name__ == '__main__':
    logger.info('start print log!')
    logger.debug('do something!')
    logger.warning('somethong maybe fail!')
    logger.info('finish!')