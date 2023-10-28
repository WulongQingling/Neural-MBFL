import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback
# 发送邮件服务器地址
smtp_server = 'smtp.exmail.qq.com'

# 发送方账号
sender = 'glw@cumt.edu.cn'
# 发送方密码（或授权密码）
password = '7G96cBh464jND5sv'


def send_email(receiver = '1597721684@qq.com', subject = 'Python SMTP 测试邮件', mail_msg = '内容'):
    # # 收件方邮箱
    # receiver = '1597721684@qq.com'
    # # 邮件标题
    # subject = 'Python SMTP 测试邮件'
    # # 邮件内容
    # mail_msg = 'Python 测试邮件发送。。。。'

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，html 设置文本格式为html格式  第三个 utf-8 设置编码
    message = MIMEText(mail_msg, 'plain', 'utf-8')  # 发送内容 （文本内容，发送格式，编码格式）
    # 发送地址
    message['From'] = sender
    # 接受地址
    message['To'] = receiver
    # 邮件标题
    message['Subject'] = Header(subject, 'utf-8')

    try:
        # 创建SMTP对象
        smtp = smtplib.SMTP()

        # 连接服务器
        smtp.connect(smtp_server)

        # 登录邮箱账号
        smtp.login(sender, password)

        # 发送账号信息
        smtp.sendmail(sender, receiver, message.as_string())
        print('success:发送成功')
    except smtplib.SMTPException:
        print('error:邮件发送失败')
        # 打印堆栈
        traceback.print_exc()
    finally:
        # 关闭
        smtp.quit()

if __name__ == '__main__':
    send_email(receiver='changzexing687@163.com', subject='Python SMTP 测试邮件', mail_msg='内容')