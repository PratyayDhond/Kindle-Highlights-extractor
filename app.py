from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', name='Pratyay')


def scrapeData(rawFile):
    with open(rawFile,'r') as input:
        inputDict = input.readlines()
        print(inputDict)

scrapeData('My Clippings.txt')