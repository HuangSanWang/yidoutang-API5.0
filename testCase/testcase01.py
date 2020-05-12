import requests
import unittest
from common.readExcel import ReadExcel
from config.readConfig import ReadConfig
from log.Log import logger
import json


logger = logger


class AccountLogin(unittest.TestCase):
    """
        登录接口-登录成功
    """
    def setUp(self) :
        # 接口请求地址
        self.url = ReadConfig().get_https('beta') + ReadExcel().get_xls('testCase.xlsx', 'login')[0][1]
        # 请求头信息
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'appos': 'ios',
            'appos-version': '4.9.5'
        }

    def tearDown(self) :
        pass

    def testcase01(self):
        self.CheckResult()

    def CheckResult(self):
        """
            断言检查
        """
        # 请求参数
        self.data = json.loads(ReadExcel().get_xls('testCase.xlsx', 'login')[0][2])

        # 异常处理，断言检查
        try:
            r = requests.post(url=self.url, data=self.data, headers=self.headers)
            # 对返回的内容进行json解码
            json_r = r.json()
            # 断言检查，返回的message是否为登录成功！
            self.assertEqual(json_r['message'], '登录成功！')
            logger.info('接口调试成功！')
            logger.info('响应内容：{}'.format(json_r))
        except Exception as e:
            logger.error('错误信息：' + e)


if __name__ == '__main__':
    AccountLogin()