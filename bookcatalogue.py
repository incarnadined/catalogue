import barcodescanner
import threading
import requests
import shutil
import json

found = ['']
isbn = ''

def liveStream():
    scanner = barcodescanner.liveScan()
    for value in scanner.run():
        if value not in found:
            found.append(value)
        print(value)
    

def checkISBN(isbn):
    if len(isbn) != 13:
        if len(isbn) != 0:
            print('{} is an invalid ISBN'.format(isbn))
        return False
    try:
        isbnlist = [int(x) for x in isbn]
    except ValueError as e:
        raise e

    print (isbnlist)
    sumofisbn = 0
    
    for x in range(12):
        if x % 2 == 0:
            sumofisbn+=isbnlist[x]
        else:
            sumofisbn+=isbnlist[x]*3

    print (10-sumofisbn%10)
    print (isbnlist[12])

    if isbnlist[12] == 10-sumofisbn%10:
        return True
    elif 10-sumofisbn%10 == 10 and isbnlist[12] == 0:
        return True
    
    print (sumofisbn)

def getData(isbn):
    response = requests.get('https://openlibrary.org/api/books?format=json&jscmd=data&bibkeys=ISBN:'+isbn)
    if response.status_code != 200:
        print ('Error '+response.status_code)
        return

    book = response.json()
    print(json.dumps(book,sort_keys=True, indent=4))
    book = book['ISBN:'+isbn]

    print(book.keys())
    cover = book['cover']['large']
    
    image = requests.get(cover, stream=True)
    if image.status_code == 200:
        with open('images/'+isbn+'large.jpg', 'wb') as f:
            image.raw.decode_content = True
            shutil.copyfileobj(image.raw, f)
            
    return book

if __name__ == '__main__':

    '''isbn=input()
    while checkISBN(isbn) != True:
        isbn = input('hello ')'''
    thread = threading.Thread(target = liveStream)
    thread.start()
    
    while True:
        #print(found)
        while checkISBN(isbn) != True:
            isbn = str(found[-1])
            print(type(isbn))
    
        print('ISBN validated')
        book = getData(isbn)
    
