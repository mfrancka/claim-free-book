from email.mime.text import MIMEText
import os
import requests
import smtplib
import datetime


def send_by_email(subject, message):
    host = os.environ['MAIL_SMTP_URL']
    username = os.environ['MAIL_USERNAME']
    password = os.environ['MAIL_PASSWORD']
    email_address = os.environ['MAIL_ADDRESS']

    msg = MIMEText('Book of the day is: {}'.format(message))
    msg['Subject'] = '"{} - new book"'.format(subject)
    msg['From'] = email_address

    s = smtplib.SMTP(host, 587)
    s.starttls()
    s.login(username, password)
    for address in ['your_email_address', ]:
        del msg['To']
        msg['To'] = address
        print(msg['To'])
        # Send the message via our own SMTP server.
        s.send_message(msg)
        s.rset()
    s.quit()


def main():
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
    print(description)
    print(send_by_email(book_title, description))
    return book_title

if __name__ == '__main__':
    main()
