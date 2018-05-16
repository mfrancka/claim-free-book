from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import os
import requests
import smtplib


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
    page = requests.get('https://www.packtpub.com/packt/offers/free-learning',
                         headers={'User-Agent':'curl'})

    soup = BeautifulSoup(page.content, 'html.parser')
    book_title = soup.find_all('div', class_='dotd-title')[0].find('h2')\
                               .next_element.lstrip().rstrip()
    description = soup.div.find(class_='dotd-main-book-summary')\
                      .find_all('div')[2].get_text().rstrip().lstrip()

    description += "\n\n https://www.packtpub.com/packt/offers/free-learning?from=block"
    print(description)
    print(send_by_email(book_title, description))
    return book_title

if __name__ == '__main__':
    main()
