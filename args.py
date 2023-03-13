import argparse
import datetime
from spider import main
from mail_sender import send_email

def today():
    today = datetime.datetime.today()
    date_string = today.strftime('%Y-%m-%d')
    print(date_string)
    return date_string

# 创建 ArgumentParser 对象，用于处理命令行参数
parser = argparse.ArgumentParser(description='一个简单的命令行接口示例')

# 添加命令行参数
parser.add_argument('--index',required=False, default=None, help='输入文件编号')
#email
parser.add_argument('--sender',required=True, help='输入发送邮箱')
parser.add_argument('--ps',required=True, help='输入邮箱密码')
parser.add_argument('--recipient',required=True, help='输入收件人邮箱')
parser.add_argument('--smtp_server',required=True, help='输入smtp_server')
parser.add_argument('--port',required=True, help='输入smtp_server的端口')

# 解析命令行参数
args = parser.parse_args()

# 将版本号写入文件
with open('DATE', 'w') as f:
    f.write(f'DATE={today()}\n')

file_path=main(args.index)

send_email(args.sender,args.ps,args.recipient,args.smtp_server,args.port,subject='Movielens-1m',attachment_path=file_path)