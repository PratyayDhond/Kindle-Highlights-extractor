from flask import Flask, render_template, request
from scraper import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', name='Pratyay')

@app.route('/fileSubmitted', methods=['GET','POST'])
def fileSubmitted():
    f = request.files['file']
    secure_filename(f.filename)

    if os.path.exists('Uploads') == False:
        os.system('mkdir Uploads')
    f.save('Uploads/MyClippings.txt')

    bookData = []
    bookData = scrapeData('Uploads/MyClippings.txt')

    for book in bookData:
        with open('tempFile.md','w') as md:
           md.write(f"## {book.getTitle()}\n")
           md.write(f"by _{book.getAuthor()}_\n")
           md.write("____\n")
           md.write("<br>\n")
           for quote in book.getQuotes():
#               md.write(f"\" {quote['quote']} \"<br>\n")
               md.write(f"\> {quote['quote']} <br>\n")
               md.write(f"<font size=\"0.1\">{quote['locationPrefix']} _{quote['location']}_ | {quote['timestamp']} </font><br><br>")
           # md.write(f"<h2 style='text-align:centre'> {book.getTitle()} </h2><br>\n")
           # md.write(f"<h4 style='text-align:right; padding-left:20vw'> - {book.getAuthor()} </h4><br>")

        if os.path.exists('outputPdfs') == False:
            os.system('mkdir outputPdfs')
        
        os.system(f'md2pdf --o outputPdfs/"{book.getTitle()}.pdf" tempFile.md')

    return render_template('fileSubmitted.html',file=f.filename)
