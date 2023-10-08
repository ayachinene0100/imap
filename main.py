from imbox import Imbox
import schedule
from datetime import date
from pathlib import Path
from os import path
from time import sleep

imap = Imbox(
    hostname='imap.qq.com',
    username='a@qq.com',
    password='1bidowq',
    ssl=False
)

my_email = 'b@qq.com'

download_dir = "C:\\downloads"
Path(download_dir).mkdir(exist_ok=True)


def download_attachments():
    messages = imap.messages(
        folder='INBOX',
        date__on=date.today(),
        sent_from=my_email,
        unread=True
    )
    for uid, message in messages:
        for attach in message.attachments:
            print(f'Downloading {attach["filename"]} ...', end=' ')
            with open(path.join(download_dir, attach['filename']), 'wb') as f:
                f.write(attach['content'].getbuffer())
            print('Done')

        imap.delete(uid)


schedule.every(1).seconds.do(download_attachments)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        sleep(1)
