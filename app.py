from flask import Flask, render_template, request, send_file
from scraper import *
from werkzeug.utils import secure_filename
import os
import threading
from time import sleep

app = Flask(__name__, static_folder="Static/")
app.config["SECRET_KEY"] = "asfasfagas"


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", name="Pratyay")


def cleanFiles():
    print("Removing highlights...")
    os.system("rm -r highlights")
    print("Highlights Removed successfully...")

    print("Removing Uploads...")
    os.system("rm -r Uploads")
    print("Uploads Removed successfully...")

    print("Removing Output...")
    os.system("rm -r output")
    print("Removed Output successfully...")

    print("Removing MD file...")
    os.system("mv README.md readme.md1")
    os.system("rm *.md")
    os.system("mv readme.md1 README.md")
    print("Removed MD File successfully...")


class Time:
    def __init__(self, timestamp):
        timestampParts = timestamp.split(" ")
        temp = timestampParts[0].split(",")
        timestampParts[0] = temp[0]
        temp = timestampParts[2].split(",")
        timestampParts[2] = temp[0]
        # print(timestampParts)
        temp = timestampParts[4].split(":")
        # timestampParts[7] = timestampParts[5]
        timestampParts[4] = temp[0]
        timestampParts.append(temp[2])
        timestampParts.append(temp[1])
        temp = timestampParts[5]
        timestampParts[5] = timestampParts[7]
        timestampParts[7] = temp
        # print(timestampParts)
        self.year = int(timestampParts[3])
        self.month = self.getMonth(timestampParts[1])
        self.date = int(timestampParts[2])
        self.hour = int(timestampParts[4])
        self.minute = int(timestampParts[5])
        self.second = int(timestampParts[6])
        if timestampParts[7] == "AM":
            self.postfix = 0
        else:
            self.postfix = 1
        # self.display()

    def getMonth(self, month):
        if month == "January":
            return 1
        if month == "February":
            return 2
        if month == "March":
            return 3
        if month == "April":
            return 4
        if month == "May":
            return 5
        if month == "June":
            return 6
        if month == "July":
            return 7
        if month == "August":
            return 8
        if month == "September":
            return 9
        if month == "October":
            return 10
        if month == "November":
            return 11
        if month == "December":
            return 12

    def display(self):
        print(f"{self.date}", end=" ")
        print(f"{self.month}", end=" ")
        print(f"{self.year}", end=" ")
        print(f"{self.hour}:{self.minute}:{self.second}", end=" ")
        print(f"{self.postfix}", end=" ")


def compareTimings(recentQuote, newQuote):
    # year is different
    if recentQuote.year > newQuote.year:
        return recentQuote
    if recentQuote.year < newQuote.year:
        return newQuote

    # year is same
    if recentQuote.month > newQuote.month:
        return recentQuote
    if recentQuote.month < newQuote.month:
        return newQuote

    # month is same
    if recentQuote.date > newQuote.date:
        return recentQuote
    if recentQuote.date < newQuote.date:
        return newQuote

    # date is same
    if recentQuote.postfix > newQuote.postfix:
        return recentQuote
    if recentQuote.postfix < newQuote.postfix:
        return newQuote

    # postfix is same
    if recentQuote.hour > newQuote.hour:
        return recentQuote
    if recentQuote.hour < newQuote.hour:
        return newQuote

    # minute is same
    if recentQuote.minute > newQuote.minute:
        return recentQuote
    if recentQuote.minute < newQuote.minute:
        return newQuote

    # second is same
    if recentQuote.second > newQuote.second:
        return recentQuote
    if recentQuote.second < newQuote.second:
        return newQuote

    return recentQuote


@app.route("/download", methods=["GET", "POST"])
def download():
    f = request.files["file"]
    secure_filename(f.filename)
    print("5% done")
    if os.path.exists("Uploads") == False:
        os.system("mkdir Uploads")
    f.save("Uploads/MyClippings.txt")
    recentBook = []

    bookData = []
    threads = []
    bookData = scrapeData("Uploads/MyClippings.txt")
    recentTime = Time(bookData[0].quotes[0]["timestamp"])
    recentBook = bookData[0]
    # recentTime.display()
    for book in bookData:
        title = book.getTitle()
        with open(f"{title}.md", "w") as md:
            md.write(
                f"<div style='font-size:36px; text-align:center;'><b>{title}</b></div>\n"
            )
            if book.getAuthor().rstrip() == "":
                pass
            else:
                md.write(f"<p style='text-align:end;'> \- by _{book.getAuthor()}_<p>\n")
            print(title)
            md.write("____\n")
            md.write("<br>\n")
            for quote in book.getQuotes():
                time = Time(quote["timestamp"])
                recentTime = compareTimings(recentTime, time)
                if recentTime == time:
                    recentBook = book
                md.write(f"“{quote['quote']}”\n<br>")
                md.write(
                    f"<span style='font-size:12px'>{quote['locationPrefix']} _{quote['location']}_ | {quote['timestamp']} </span><br><br>"
                )
        if os.path.exists("highlights") == False:
            os.system("mkdir highlights")
        str = f'md2pdf --o "highlights/{title}.pdf" "{title}.md" '
        t = threading.Thread(target=os.system, args=(str,))
        threads.append(t)
        t.start()

    # recentBook.display()
    title = recentBook.getTitle()
    with open(f"{title}.md", "w") as md:
        md.write(
            f"<div style='font-size:36px; text-align:center;'><b>{title}</b></div>\n"
        )
        if recentBook.getAuthor().rstrip() == "":
            pass
        else:
            md.write(
                f"<p style='text-align:end;'> \- by _{recentBook.getAuthor()}_<p>\n"
            )
        print(title)
        md.write("____\n")
        md.write("<br>\n")
        for quote in recentBook.getQuotes():
            md.write(f"“{quote['quote']}”\n<br>")
            md.write(
                f"<span style='font-size:12px'>{quote['locationPrefix']} _{quote['location']}_ | {quote['timestamp']} </span><br><br>"
            )
    if os.path.exists("highlights") == False:
        os.system("mkdir highlights")
    str = f'md2pdf --o "highlights/_latest.pdf" "{title}.md" '
    t = threading.Thread(target=os.system, args=(str,))
    threads.append(t)
    t.start()

    for thread in threads:
        thread.join()
    os.system(f'zip "Highlights.zip" highlights/*')
    os.system(f'mv Highlights.zip "Static/"')

    cleanFiles()
    return send_file("Static/Highlights.zip", as_attachment=True)
