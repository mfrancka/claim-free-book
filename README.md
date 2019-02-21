# Goal:
Check what a book is available for flee claim on packtpub.

# Config
If you want to send notifications by email you need to have your email account
used as a sender.
```bash
export MAIL_USERNAME=address@email.pl
export MAIL_SMTP_HOST=email.pl
export MAIL_PASSWORD=password
export MAIL_ADDRESS=email_set_as_from_in_email
export RECIPIENTS=email1,email2,email3

python free.py
```
You can also make .env file with variables above and put it where your script launch
```bash
MAIL_USERNAME=address@email.pl
MAIL_SMTP_HOST=email.pl
MAIL_PASSWORD=password
MAIL_ADDRESS=email_set_as_from_in_email
RECIPIENTS=email1,email2,email3
```

