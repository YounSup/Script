import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

host = "smtp.gmail.com"
port = "587"

def sendMail(email,data):
    global host, port
    senderAddr = "dudtjq0509@gmail.com"
    passwd = "a1024424" 

    recipientAddr = email
    title = "유기동물 정보 조회"

    msg = MIMEMultipart('alternative')

    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    msgPart = MIMEText(data, 'plain')
    msg.attach(msgPart)

    print("서버 연결중 ... ")
    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd) 
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()

    print("메일 보내기 성공!")
