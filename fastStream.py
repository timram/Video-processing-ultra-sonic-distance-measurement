import io
import threading
import picamera
import time
import serial
import cv2 as cv
import numpy as np
from LineProcessor import LineProcessor

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []
minLineLength = 5
maxLineGap = 15
ser = serial.Serial('/dev/ttyUSB0',9600)
lineProcessor = LineProcessor()

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.frameNumber = 0
        self.start()
    
    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                # Read the image and do some processing on it
                    buff = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
                 
                    img = cv.imdecode(buff, 1)
                    blur = cv.medianBlur(img, 1)
                    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
                    edges = cv.Canny(gray, 80, 120)
                    lines = cv.HoughLinesP(edges, 1, np.pi/180, 2, None, minLineLength, maxLineGap);

                    if not (lines is None):
                        pixDist = lineProcessor.ProcessLines(lines[0])
                        if not (pixDist is None):
                            coorLine = "%s-%s" %(pixDist[0], pixDist[1])
                            ser.write(coorLine)
                            print(coorLine)
                        else:
                            print "Only Horizontal Lines or not center range lines"
                    else:
                        print "No Lines"

                    self.frameNumber+=1

#                    if lines != None:
#                        for x1,y1,x2,y2 in lines[0]:
#                            cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
#                        cv.imwrite(str(self.frameNumber)+"-"+str(time.time())+"res.jpeg", img)
#

                    if self.frameNumber==100:
                        done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(4)]
    camera.resolution = (800, 50)
    camera.framerate = 90
    camera.start_preview()
    time.sleep(2)
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()