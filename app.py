from flask import Flask, render_template, request, send_file
from scraper import *
from werkzeug.utils import secure_filename
import os
import platform

app = Flask(__name__, static_folder="Static/")
app.config['SECRET_KEY'] = "asfasfagas"

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html', name='Pratyay')

@app.route('/download', methods=['GET','POST'])
def download():
    f = request.files['file']
    secure_filename(f.filename)
    print("5% done")
    if os.path.exists('Uploads') == False:
        os.system('mkdir Uploads')
    f.save('Uploads/MyClippings.txt')

    bookData = []
    bookData = scrapeData('Uploads/MyClippings.txt')
    for book in bookData:
        title = book.getTitle()
        with open('tempFile.md','w') as md:
#           md.write(f"<h2>{title}</h2>\n")
            md.write(f"<div style='font-size:36px; text-align:center;'><b>{title}</b></div>\n")
#           md.write(f"<p style='position:absolute; right:0; padding-right:20px;'>by _{book.getAuthor()}_<p>\n")
            if book.getAuthor().rstrip() == '':
                pass
            else:
                md.write(f"<p style='text-align:end;'> \- by _{book.getAuthor()}_<p>\n")
            print(title)
            md.write("____\n")
            md.write("<br>\n")
            for quote in book.getQuotes():
               md.write(f"“{quote['quote']}”\n<br>")
               md.write(f"<span style='font-size:12px'>{quote['locationPrefix']} _{quote['location']}_ | {quote['timestamp']} </span><br><br>")
        if os.path.exists('highlights') == False:
           os.system('mkdir highlights')
        os.system(f'md2pdf --o highlights/"{title}.pdf" tempFile.md')

    # if platform.platform() == 'Windows':
        # os.system(f'zip Highlights.zip highlights')
    # else:
        # os.system(f'tar -cf Highlights.tar highlights')    
    os.system(f'zip "Highlights.zip" highlights/*')
    os.system(f'mv Highlights.zip "Static/"')

    print('Removing Uploads...')
    os.system('rm -r Uploads')
    print('Uploads Removed successfully...')
    
    print('Removing highlights...')
    os.system('rm -r highlights')
    print('Highlights Removed successfully...')
    
    print('Removing Output...')
    os.system('rm -r output')
    print('Removed Output successfully...')

    print('Removing MD file...')
    os.system('rm tempFile.md')
    print('Removed MD File successfully...')


    return send_file('Static/Highlights.zip', as_attachment=True)
    
    # return send_from_directory(directory= 'Static' ,path='Static/Highlights.zip',filename='Highlights.zip')
    # return render_template('fileSubmitted.html',file=f.filename)
