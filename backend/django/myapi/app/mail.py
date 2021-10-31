import smtplib, ssl
import os
from dotenv import load_dotenv

load_dotenv()

def send_mail(receiver, contents):
    smtp_server = 'smtp.gmail.com'
    port = 587  # starttls
    sender = os.getenv('LOGIN')
    password = os.getenv('PW')

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender, password)
        server.sendmail(sender, receiver, contents)
    except Exception as e:
        print(e)
    finally:
        server.quit()


if __name__ == '__main__':
    send_mail(os.getenv('LOGIN'), 'Subject: Test\n\nTest')
