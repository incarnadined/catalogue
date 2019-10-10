from pyzbar import pyzbar
from imutils.video import VideoStream
import imutils
import time
import cv2

class liveScan():
    
    def run(data=''):
        found = []
        vs = VideoStream(src=0).start()
        time.sleep(2)

        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            barcodes = pyzbar.decode(frame)
            #print(barcodes)

            for barcode in barcodes:
                #print(barcode)
                x,y,w,h = barcode.rect
                cv2.rectangle(frame, (x,y),(x+w, y+h), (0,0,255), 2)
    
                barcodeData = barcode.data.decode('utf-8')
                barcodeType = barcode.type

                text = '{}({})'.format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

                if barcodeData not in found:
                    found.append(barcodeData)
                yield found
            cv2.imshow('Image', frame)
            cv2.waitKey(1) & 0xFF

liveScan()
