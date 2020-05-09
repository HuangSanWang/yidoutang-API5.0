"""
    封装读取Excel表格的函数
"""
import os
import getpathinfo
from xlrd import open_workbook
from log.Log import logger


# 拿到该项目所在的绝对路径
path = getpathinfo.get_path()
logger = logger


class ReadExcel(object):

    def get_xls(self, xls_name, sheet_name):  # xls_name填写用例的Excel名称 sheet_name该Excel的sheet名称
        cls = []
        # 获取用例文件的路径
        xls_path = os.path.join(path, 'testFile', xls_name)
        # 打开Excel文件
        wb = open_workbook(xls_path)
        # 打开该Excel文件内的sheet
        ws = wb.sheet_by_name(sheet_name)
        # 获取该sheet内容的行数
        nrows = ws.nrows
        for i in range(nrows):  # 根据行数进行循环遍历
            # 如果这个Excel的这个sheet的第i行的第一列不等于case_name那么我们把这行的数据添加到cls[]
            if ws.row_values(i)[0] != u'case_name':
                cls.append(ws.row_values(i))
        return cls


if __name__ == '__main__':
    print(ReadExcel().get_xls('testCase.xlsx', 'login')[0][2])