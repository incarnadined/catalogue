from PIL import Image, ImageTk
import barcodescanner
import tkinter as tk
import threading
import requests
import shutil
import json
import glob

canvas = tk.Tk()
found = ['1']
isbn = ['1']
scanned = []

def mainLoop():
    canvas.mainloop()

def liveStream():
    scanner = barcodescanner.liveScan()
    for value in scanner.run():
        if value not in found:
            found.append(value)
        print(value)
    

def checkISBN(isbn):
    #print(isbn)
    isbn = isbn[-1]
    
    status=glob.glob('./'+isbn+'*.jpg')
    if status != []:
        print(status)
        return False
    
    if len(isbn) != 13:
        if len(isbn) != 0:
            if isbn != '1':
                print('{} is an invalid ISBN'.format(isbn))
        return False
    try:
        isbnlist = [int(x) for x in isbn]
    except ValueError as e:
        raise e

    #print (isbnlist)
    sumofisbn = 0
    
    for x in range(12):
        if x % 2 == 0:
            sumofisbn+=isbnlist[x]
        else:
            sumofisbn+=isbnlist[x]*3

    #print (10-sumofisbn%10)
    #print (isbnlist[12])

    if isbnlist[12] == 10-sumofisbn%10:
        return True
    elif 10-sumofisbn%10 == 10 and isbnlist[12] == 0:
        return True
    
    #print (sumofisbn)

def getData(isbn):
    if isbn[-1][0] != '9': #Misread barcode
        isbn[-1] = '9'+isbn[-1][1:]
        #print(isbn)
        
    response = requests.get('https://openlibrary.org/api/books?format=json&jscmd=data&bibkeys=ISBN:'+isbn[-1])
    if response.status_code != 200:
        print ('Error '+response.status_code)
        return

    book = response.json()
    if book == {}:
        print('Book not found')
        return False
    
    print(json.dumps(book,sort_keys=True, indent=4))
    #print(book.keys())

    book = book[list(book.keys())[0]]

    #print(book.keys())
    cover = book['cover']['large']
    
    image = requests.get(cover, stream=True)
    if image.status_code == 200:
        with open('images/'+isbn[-1]+'large.jpg', 'wb') as f:
            image.raw.decode_content = True
            shutil.copyfileobj(image.raw, f)

    print(book['title'])
    '''print(book['authors']['name'])
    print(book['publishers']['name'])'''
    w = tk.Label(canvas,text=book['title'])
    w.pack()

    '''z = tk.Label(canvas, text=book['authors']['name'])
    z.pack()

    x = tk.Label(canvas, text='and published by '+book['publishers']['name'])
    x.pack()'''

    image = Image.open('images/'+isbn[-1]+'large.jpg')
    photo = ImageTk.PhotoImage(image)

    window = tk.Canvas(canvas)
    window.pack()
    window.create_image(0, 0, image=photo, anchor=tk.NW)   

    #window = threading.Thread(target = canvas.mainloop)
    #window.start()
    canvas.mainloop()

    scanned.append(isbn[-1])
    return book

if __name__ == '__main__':

    '''isbn=input()
    while checkISBN(isbn) != True:
        isbn = input('hello ')'''
    thread = threading.Thread(target = liveStream)
    thread.start()
    
    while True:
        while checkISBN(isbn) != True:
            isbn = found[-1]
                         
    
        print('ISBN validated')
        book = getData(isbn)   
