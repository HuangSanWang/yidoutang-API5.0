import HTMLTestRunner
import os
import getpathinfo
from config.configEmail import Fox_Mail
from log.Log import logger
import unittest
from config.readConfig import ReadConfig


# 获取项目地址
path = getpathinfo.get_path()
# 获取测试报告存放的目录
report_path = os.path.join(path, 'result')
# 从config文件中读取邮件发送开关
on_off = ReadConfig().get_email('on_off')
logger = logger


class AllTest:
    """
        定义一个AllTest类
    """
    def __init__(self):
        """
            初始化参数
        """
        global resultPath
        # 测试报告地址
        resultPath = os.path.join(report_path, 'report.html')
        # 执行测试文件的配置文件路径
        self.caseListFile = os.path.join(path, 'caselist.txt')
        # 测试文件断言路径
        self.caseFile = os.path.join(path, 'testCase')
        self.caseList = []
        # 将resultPath,caseListFile和caseList的值输入到日志，方便定位查看问题
        logger.info('resultPath = ' + resultPath)
        logger.info('caseListFile = ' + self.caseListFile)
        logger.info('caseList = ' + str(self.caseList))

    def set_case_list(self):
        """
            读取caselist.txt文件中的用例名称，并添加到caselist元素组
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            # 判定data非空且不以#开头
            if data != '' and not data.startswith('#'):
                # 读取每行数据会将换行转换为\n，去掉每行数据中的\n
                self.caseList.append(data.replace('\n', ''))
        # 关闭文件
        fb.close()

    def set_case_suite(self):
        """
            获取测试集
        """
        # 通过set_case_list()拿到caselist元素组
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []
        for case in self.caseList:
            # 通过split函数来将aaa/bbb分割字符串，-1取后面，0取前面
            case_name = case.split('/')[-1]
            # 批量加载用例，第一个参数为用例存放路径，第二个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            # 将discover存入suite_module元素组
            suite_module.append(discover)

        # 判断suite_module元素组是否存在元素
        if len(suite_module) > 0:
            # 如果存在，循环取出元素组内容，命名为suite
            for suite in suite_module:
                # 从discover中取出test_name，使用addTest添加到测试集
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            logger.error('suite_module元素组不存在元素!')
            return None

        # 返回测试集
        return test_suite

    def run(self):
        """
            执行测试用例并生成测试报告
        """
        try:
            # 调用set_case_suite获取test_suite
            suit = self.set_case_suite()
            # 判定test_suite是否为空
            if suit is not None:
                # 打开result/report.html测试报告文件，如果不存在就创建
                fp = open(resultPath, 'wb')
                # 调用HTMLTestRunner
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='接口测试报告', description='一兜糖接口自动化测试')
                runner.run(suit)
            else:
                logger.warning('测试集内无用例！')
        except Exception as e:
            logger.error('错误信息：' + str(e))

        finally:
            logger.info('*********TEST END*********')
            # 关闭文件
            fp.close()

        # 判断邮件开关
        if on_off == 'on':
            Fox_Mail().fox_mail()
        else:
            logger.warning('邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告')


if __name__ == '__main__':
    AllTest().run()