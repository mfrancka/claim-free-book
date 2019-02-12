from email.mime.text import MIMEText
import os
import requests
import smtplib
import datetime
from dotenv import load_dotenv

class Notifier:
    def __init__(self, host, username, password, email_address):
        self.host = host
        self.username =  username
        self.password = password
        self.email_address = email_address

    def send_by_email(self, subject, message, recipients):
        msg = MIMEText('Book of the day is: {}'.format(message))
        msg['Subject'] = '"{} - new book"'.format(subject)
        msg['From'] = self.email_address

        s = smtplib.SMTP(self.host, 587)
        s.starttls()
        s.login(self.username, self.password)
        for address in recipients:
            del msg['To']
            msg['To'] = address
            print(msg['To'])
            # Send the message via our own SMTP server.
            s.send_message(msg)
            s.rset()
        s.quit()


def main():
    load_dotenv()
    host = os.environ['MAIL_SMTP_HOST']
    username = os.environ['MAIL_USERNAME']
    password = os.environ['MAIL_PASSWORD']
    email_address = os.environ['MAIL_ADDRESS']
    recipients = os.environ['RECIPIENTS'].split(',')

    (book_title, description) = get_book()
    notifier = Notifier(host,username,password,email_address)
    print(notifier.send_by_email(book_title,description, recipients))

def get_book():
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + datetime.timedelta(days=1) 
    page = requests.get('https://services.packtpub.com/free-learning-v1/offers?dateFrom={}Z&dateTo={}Z'.format(today.isoformat(), tomorrow.isoformat()),
                         headers={'User-Agent':'curl'})

    desc = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:{}'.format(page.json()['data'][0]['productId']),
                         headers={'User-Agent':'curl'})

    description = ''
    book_title = ''
    for book in desc.json()['items']:
        book_title += book['volumeInfo']['title']
        description += book['volumeInfo']['description']

    description += "\n\n https://www.packtpub.com/packt/offers/free-learning?from=block"
    print(book_title)
    return (book_title, description)

if __name__ == '__main__':
    main()
