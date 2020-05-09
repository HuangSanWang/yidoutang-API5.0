import requests
from common.readExcel import ReadExcel
from config.readConfig import ReadConfig
import json


def login():
    url = ReadConfig().get_https('beta') + ReadExcel().get_xls('testCase.xlsx', 'login')[0][1]
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'appos': 'ios',
        'appos-version': '4.9.5'
    }
    data = json.loads(ReadExcel().get_xls('testCase.xlsx', 'login')[0][2])

    r = requests.post(url=url, data=data, headers=headers)
    json_r = r.json()

    if json_r['message'] == '登录成功！':
        print('接口调试通过！')
    else:
        print('调试失败！')
    print(json_r)
    print(json_r['data']['token'])


if __name__ == '__main__':
    login()