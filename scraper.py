endOfHighlight = '=========='

class Book:
    
    def __init__(self,author,bookName):
        self.author = author
        self.bookName = bookName
        self.quotes = [] # A list of Dictionaries -> Quote, Quote Time, Quote Location
    
    def getAuthorName(self):
        return self.author
    
    def getBooKName(self):
        return self.bookName
    
    def getQuotes(self):
        return self.quotes

def scrapeData(inputFile):
    rawData = readData(inputFile)
    author='-'
    bookName=''
    quote=''
    timestamp=''
    location=''
    for i in range(4,len(rawData),5):
        
        # Working on accessing the bookname and author name
        BookNameAndAuthor = rawData[i-4]
        strLen = len(BookNameAndAuthor)
        j = strLen - 1
        # Checking if the book has author information or not | If there is author it would be specified with '* ( _Author Name_) '
        if BookNameAndAuthor[-2] == ')':
            while BookNameAndAuthor[j] != '(':
                j-=1
            endIndex = len(BookNameAndAuthor)-2
            author = BookNameAndAuthor[j+1:endIndex]
        bookName = BookNameAndAuthor[:j]

        ## Getting timestamp and location of quote from data
        contains = rawData[i-3].find('page')
        locationPrefix = ''
        if contains == -1:
            locationPrefix = 'Location '
        else:
            locationPrefix = 'Page No. '

        locationEndIndex = rawData[i-3].index('|') - 1
        locationStartIndex = locationEndIndex-1
        while rawData[i-3][locationStartIndex] != ' ':
            locationStartIndex-=1
        locationStartIndex+=1
        timestampStartIndex = rawData[i-3].index('| Added on') + 9

        location = rawData[i-3][locationStartIndex:locationEndIndex]
        timestamp = rawData[i-3][timestampStartIndex+2:]

        ## Getting Quote from the data
        
        quote = rawData[i-1]
        print(bookName)
        print(author)
        print(locationPrefix + location)
        print(timestamp)
        print(quote)


def readData(rawFile):
    with open(rawFile,'r') as input:
        inputList = input.readlines()
        return inputList


op = scrapeData('My Clippings.txt')