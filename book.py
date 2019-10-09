import requests
import shutil

def checkISBN(isbn):
    if len(isbn) != 13:
        print('ISBN invalid')
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

    if isbnlist[12] == 10-sumofisbn%10:
        return True

    print (sumofisbn)

def getData(isbn):
    response = requests.get('https://openlibrary.org/api/books?format=json&jscmd=data&bibkeys=ISBN:'+isbn)
    if response.status_code != 200:
        print ('Error '+response.status_code)
        return

    book = response.json()
    book = book['ISBN:'+isbn]

    print(book.keys())
    cover = book['cover']['large']
    
    image = requests.get(cover, stream=True)
    if image.status_code == 200:
        with open(isbn+'large.jpg', 'wb') as f:
            image.raw.decode_content = True
            shutil.copyfileobj(image.raw, f)
            
    return book

if __name__ == '__main__':

    isbn=input()
    while checkISBN(isbn) != True:
        isbn = input()

    
    print('ISBN validated')
    book = getData(isbn)
    
