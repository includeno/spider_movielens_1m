import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(sender,password,recipient,smtp_server,port,subject = 'Test Email with Attachment',attachment_path = 'links.csv'):
    # 设置邮件相关参数
    body = 'Please see the attached file.'

    # 创建 MIMEMultipart 对象
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject

    # 添加邮件正文
    text = MIMEText(body)
    message.attach(text)

    # 添加附件
    with open(attachment_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='csv')
        attachment.add_header('Content-Disposition', 'attachment', filename=f.name)
        message.attach(attachment)

    # 发送邮件
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recipient, message.as_string())
    server.quit()
