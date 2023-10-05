import os

endOfHighlight = "=========="


class Book:
    def __init__(self, author, bookName):
        self.author = author
        self.bookName = bookName
        self.quotes = (
            []
        )  # A list of Dictionaries -> Quote, Quote Time, Quote Location, location prefix

    def getAuthor(self):
        return self.author

    def getTitle(self):
        return self.bookName

    def getQuotes(self):
        return self.quotes

    def addQuote(self, quote, timestamp, location, locationPrefix, quote_type=None):
        quote = {
            "quote": quote,
            "timestamp": timestamp,
            "location": location,
            "locationPrefix": locationPrefix,
            "type": quote_type,
        }
        for a in self.quotes:
            if a["quote"] == quote["quote"]:
                return
        self.quotes.append(quote)
        return

    def display(self):
        print(f"{self.bookName}", end=" ")
        print(f"{self.author}")
        print(f"{self.quotes}", end=" ")


# Stores the quotes for all the books
books = []
recentBook = []


def bookExist(book):
    for a in books:
        if book.rstrip() == a.getTitle().rstrip():
            return a
    else:
        return -1


# Testing Feature, used to create files for different books
def outputToTxt():
    if os.path.exists("output") == False:
        os.system("mkdir output")
    for a in books:
        with open(f"output/{a.getTitle()}.txt", "w") as highlights:
            # print(a.getTitle())
            highlights.write(f"Author : {a.getAuthor()}\n")
            highlights.write(f"Title  : {a.getTitle()}\n")
            highlights.write("\n\n")
            highlights.write(
                "------------------------------------------------------------------------------------------------------------------\n"
            )
            for q in a.getQuotes():
                for k in q.keys():
                    highlights.write(k + " -> " + q[k] + "\n")
                highlights.write("---------\n")
            highlights.write(
                "------------------------------------------------------------------------------------------------------------------"
            )


def scrapeData(inputFile):
    rawData = readData(inputFile)
    author = ""
    bookName = ""
    quote = ""
    timestamp = ""
    location = ""
    i = 0

    while i < len(rawData):
        quote = ""
        author = ""
        if i == len(rawData) - 1:
            break

        while (
            i < len(rawData)
            and rawData[i].rstrip() == ""
            or rawData[i].rstrip() == endOfHighlight
        ):
            if i < len(rawData) == False:
                break
            else:
                i += 1

        # Working on accessing the bookname and author name
        BookNameAndAuthor = rawData[i]
        strLen = len(BookNameAndAuthor)
        j = strLen - 1
        # Checking if the book has author information or not | If there is author it would be specified with '* ( _Author Name_) '
        if BookNameAndAuthor[-2] == ")":
            while BookNameAndAuthor[j] != "(":
                j -= 1
            endIndex = len(BookNameAndAuthor) - 2
            author = BookNameAndAuthor[j + 1 : endIndex].rstrip()
        bookName = BookNameAndAuthor[:j].rstrip()

        i += 1

        ## Getting timestamp and location of quote from data
        contains = rawData[i].find("page")
        locationPrefix = ""
        if contains == -1:
            locationPrefix = "loc "
        else:
            locationPrefix = "Page No. "
        locationEndIndex = rawData[i].find("|") - 1

        locationStartIndex = locationEndIndex - 1
        try:
            while i < len(rawData) and rawData[i][locationStartIndex] != " ":
                locationStartIndex -= 1
            locationStartIndex += 1
        except:
            pass
        timestampStartIndex = rawData[i].find("| Added on") + 9

        location = rawData[i][locationStartIndex:locationEndIndex].rstrip()
        timestamp = rawData[i][timestampStartIndex + 2 :].rstrip()

        ## Getting Quote type from the data
        quote_type = None
        if "Your Note on" in rawData[i]:
            quote_type = "Note"
        elif "Your Highlight on" in rawData[i]:
            quote_type = "Highlight"

        i += 2
        ## Getting Quote from the data
        while i < len(rawData) and rawData[i].rstrip() != endOfHighlight:
            quote += rawData[i].rstrip() + "\n"
            i += 1
        quote = quote.rstrip()
        if quote == "":
            continue
        book = bookExist(bookName)
        if book == -1:
            tempBook = Book(author, bookName)
            tempBook.addQuote(quote, timestamp, location, locationPrefix, quote_type)
            books.append(tempBook)
        else:
            book.addQuote(quote, timestamp, location, locationPrefix, quote_type)
    # outputToTxt()

    return books


def readData(rawFile):
    with open(rawFile, "r") as input:
        inputList = input.readlines()
        return inputList


op = scrapeData("My Clippings.txt")
outputToTxt()
