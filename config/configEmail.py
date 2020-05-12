"""
    封装测试报告邮件发送函数
"""
import os
import getpathinfo
import time
from config import readConfig
from log.Log import logger
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


read_conf = readConfig.ReadConfig()
# 从config文件中读取邮件主题
subject = read_conf.get_email('subject') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
# 从config文件中读取发件人
fromaddr = read_conf.get_email('from')
# 从config文件中读取收件人
addressee = read_conf.get_email('addressee')
# 从config文件中读取抄送人
cc = read_conf.get_email('cc')

# foxmail邮箱的SMTP服务器及端口
foxsmtpserver = 'smtp.yidoutang.com'
foxport = 25
# 发件人邮箱名及密码
foxusername = 'huangsw@yidoutang.com'
foxpassword = 'hsw52013140..'
# 获取测试报告路径
report_path = os.path.join(getpathinfo.get_path(), 'result', 'report.html')
logger = logger


class Fox_Mail(object):

    def fox_mail(self):
        # 初始化邮件对象
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = addressee
        msg['Cc'] = cc
        msg['Subject'] = subject

        # 邮件正文
        content = """
                HI:
                        附件为本次接口测试报告，请查阅！！！
                        """

        # 附件
        reportApart = MIMEApplication(open(report_path, 'rb').read())
        reportApart.add_header('Content-Disposition', 'attachment', filename=report_path)
        # 附加邮件内容
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        msg.attach(reportApart)

        # 登录并发送邮件
        try:
            server = smtplib.SMTP(foxsmtpserver, foxport)
            # 使用ehlo指令向ESMTP（SMTP扩展）确认你的身份
            server.ehlo()
            # 使SMTP连接运行在TLS模式，所有的SMTP指令都会被加密
            server.starttls()
            # 设置输出debug调试信息
            server.set_debuglevel(1)
            # 登录SMTP服务器
            server.login(foxusername, foxpassword)
            # 发送邮件
            server.sendmail(fromaddr, addressee.split(','), msg.as_string())
            logger.info('邮件发送成功！！！')
            # 关闭SMTP会话
            server.quit()
        except smtplib.SMTPException as e:
            # 打印错误信息到日志
            logger.error('error:', e)


if __name__ == '__main__':
    # 调试
    print(subject)
    Fox_Mail().fox_mail()