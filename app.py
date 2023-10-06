import os
import shutil
import threading
import zipfile
from datetime import datetime
from time import sleep
from typing import List

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from scraper import scrapeData

app = Flask(__name__, static_folder="Static/")
app.config["SECRET_KEY"] = "asfasfagas"


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", name="Pratyay")


def remove_path(path: str):
    if os.path.exists(path):
        print(f"Removing {path}...")
        os.remove(path)
        print(f'{path} removed successfully...')


def clean_files():
    remove_path('highlights')
    remove_path('Uploads')
    remove_path('output')
    shutil.move('README.md', 'README.md1')
    remove_path('*.md')
    shutil.move('README.md1', 'README.md')


class Time:
    def __init__(self, timestamp):
        self.__datetime = datetime.strptime(
            timestamp, "%A, %B %d, %Y %I:%M:%S %p"
        )
        self.display()

    @property
    def date(self):
        return self.__datetime.day

    @property
    def month(self):
        return self.__datetime.month

    @property
    def year(self):
        return self.__datetime.year

    @property
    def hour(self):
        return self.__datetime.hour

    @property
    def minute(self):
        return self.__datetime.minute

    @property
    def second(self):
        return self.__datetime.second

    @property
    def postfix(self):
        return self.__datetime.strftime("%p")

    def display(self):
        print(self.__datetime.strftime('%d %m %Y %H:%M:%s %p'))

    @property
    def timestamp(self) -> float:
        return self.__datetime.timestamp()


def get_most_recent_quote(last_quote: Time, new_quote: Time):
    return max(last_quote.timestamp, new_quote.timestamp)


def build_book(book, latest_book, recent_time: Time):
    title = book.getTitle()
    content = f"<div style='font-size:36px; text-align:center;'><b>{title}</b></div>\n"
    if book.getAuthor().rstrip() != "":
        content += (
            f"<p style='text-align:end;'> \- by _{book.getAuthor()}_<p>\n"
        )
    content += "____\n<br>\n"
    for quote in book.getQuotes():
        time = Time(quote["timestamp"])
        recent_time = get_most_recent_quote(recent_time, time)
        if recent_time == time:
            latest_book = book
        if quote['type'] == 'Note':
            content += f'__Note__: {quote["quote"]}\n<br>'
        elif quote['type'] == 'Highlight':
            content += f'__Highlight__: \n\n> {quote["quote"]}\n\n<br>'
        elif quote['type'] == 'Bookmark':
            content += f'__Bookmark__: {quote["quote"]}\n<br>'
        else:
            content += f'"{quote["quote"]}"\n<br>'
        content += f"<span style='font-size:12px'>{quote['locationPrefix']} _{quote['location']}_ | {quote['timestamp']} </span><br><br>"
    return content, latest_book


def save_book(title: str, content: str) -> str:
    with open(f"{title}.md", "w") as md:
        md.write(content)
        return f"{title}.md"


def prepare_pdf(title, md_path: str) -> str:
    if not os.path.exists("highlights"):
        os.mkdir("highlights")
    return f'pandoc --pdf-engine=wkhtmltopdf "{md_path}" -o "`highlights/{title}.pdf`"'


@app.route("/download", methods=["GET", "POST"])
def download():
    f = request.files["file"]
    secure_filename(f.filename)
    print("5% done")
    if os.path.exists("Uploads") == False:
        os.mkdir("Uploads")
    f.save("Uploads/MyClippings.txt")
    threads = []
    book_data = scrapeData("Uploads/MyClippings.txt")
    latest_time = Time(book_data[0].quotes[0]["timestamp"])
    latest_book = book_data[0]
    commands = []
    # recentTime.display()
    for book in book_data:
        title = book.getTitle()
        book_content, latest_book = build_book(book, latest_book, latest_time)
        path = save_book(title, book_content)
        pdf_command = prepare_pdf(title, path)
        commands.append(pdf_command)

    for command in commands:
        t = threading.Thread(target=os.system, args=(command,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Copy latest book as the _latest.pdf
    if latest_book:
        shutil.copy(
            f'highlights/{latest_book.getTitle()}.pdf',
            'highlights/_latest.pdf',
        )

    with zipfile.ZipFile("Highlights.zip", "w") as zip:
        for file in os.listdir("highlights"):
            zip.write(f"highlights/{file}")
    shutil.move("Highlights.zip", "Static/")

    clean_files()
    return send_file("Static/Highlights.zip", as_attachment=True)
