from email.mime.text import MIMEText
import os
import requests
import smtplib
from dotenv import load_dotenv
from parsel import Selector


class Notifier:
    def __init__(self, host, username, password, email_address):
        self.host = host
        self.username = username
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

    book_informations = get_book()
    notifier = Notifier(host, username, password, email_address)
    description = make_full_description(book_informations)
    print(notifier.send_by_email(book_informations["title"], description, recipients))


def get_book():
    page = requests.get(
        'https://www.packtpub.com/free-learning', headers={'User-Agent': 'curl'}
    )
    sel = Selector(text=page.text)
    book_title = sel.xpath('//h3/text()').get()
    description = sel.xpath('//div[contains(@class, "free_learning__product_description")]/span/text()').get()
    publication_date = sel.xpath('//div[contains(@class, "free_learning__product_pages_date")]/span/text()').get().replace("Publication date:", "")
    author = sel.xpath(r'//span[re:test(@class, ".*free_learning__author")]/text()').get().replace("\n", "")
    rate = '-'.join(sel.xpath('//div[contains(@class, "product-info__rating")]/span/text()').getall())
    return {"title" : book_title, "author": author, "rate": rate, "publication_date" : publication_date ,"description" : description}


def make_full_description(book_informations):
    return f"Author: {book_informations['author']}\nRating: {book_informations['rate']}\nPublication date: {book_informations['publication_date']}\nDescription: {book_informations['description']}\n\nhttps://www.packtpub.com/free-learning"


if __name__ == '__main__':
    main()
