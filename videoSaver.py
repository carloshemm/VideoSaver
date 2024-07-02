import os
import sys
import cv2
import time
import queue
import pathlib
import argparse
import threading
import numpy as np
from datetime import datetime, timedelta, timezone
import datetime as dt

CD = pathlib.Path(__file__).parent.resolve()
os.chdir(CD)

defaultFPS = 30

def video_prop(videoPath):
    fps,width,height = None,None,None
    cap = cv2.VideoCapture(videoPath)
    if cap.isOpened():
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height =  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
    if fps is not None:
        if fps > 30:
            fps = 20
    print(f"(fps,width,height) = ({fps},{width},{height})")
    return fps,width,height

def FPSNumbers(tempo,fps):
    frames = int(tempo*60*fps)
    return frames
    

class VideoSaver:
    def __init__(self,opt):
        self.RTSP_URL = None
        self.process = False
        self.fila = queue.Queue()
        self.max_frames = 0
        self.frames_count = 0

        # Definindo o fuso horário GMT-3
        BRT = timezone(timedelta(hours=-3))


        if opt.output != None:  
            if opt.output.endswith(".mp4"):
                arquivoSaida = "VIDEOS/"+opt.output
            else:
                arquivoSaida = f"VIDEOS/-{opt.output}-.mp4"
        else:
            filename = datetime.now(BRT).strftime("%Y-%m-%d_%H:%M:%S")
            arquivoSaida = f"VIDEOS/{filename}.mp4"
        print(f"Saving video in {arquivoSaida}")
        fps,width,height = video_prop(opt.input)
        self.width = width
        self.height = height
        if (fps and width and height) != None:
            if opt.time != None:
                self.max_frames = FPSNumbers(opt.time,fps)
                self.frames_count = self.max_frames
            if opt.fps != defaultFPS:
                fps = opt.fps

            self.RTSP_URL = opt.input
            self.video_writer = cv2.VideoWriter(arquivoSaida, cv2.VideoWriter_fourcc('m','p','4','v'), fps, (width, height))
            self.cap = cv2.VideoCapture(opt.input)
            self.process = True



    def Receive(self):
        print("start Receive")
        ret, frame = self.cap.read()
        if ret:
            self.fila.put(frame)
        while self.process:
            ret, frame = self.cap.read()
            if ret:
                self.fila.put(frame)
            else:
                self.Reconnected()


    def Reconnected(self):
        while True:
            print("Reconnection try", self.RTSP_URL)
            self.cap = cv2.VideoCapture(self.RTSP_URL)
            hasFrame, frameOriginal = self.cap.read()
            if hasFrame:
                return True
            else:
                time.sleep(5)


    def Display(self):
        print("Start Displaying")

        while self.process:
            
            
            if self.fila.empty() != True:
                frame = self.fila.get()
                self.video_writer.write(frame)
                
                if self.frames_count > 0:
                    self.frames_count = self.frames_count-1
                    progresso = int((100 - (self.frames_count/self.max_frames)*100))
                    #make a progress bar using progesso
                    bar = '=' * progresso + ' ' * (100 - progresso)
                    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, progresso, '%', ''))
                    sys.stdout.flush()
                    
                    if self.frames_count == 0:
                        self.process=False

                if opt.show:
                    cv2.namedWindow("tela", cv2.WINDOW_NORMAL)
                    cv2.imshow("tela", frame)
                    key = cv2.waitKey(1)
                    if key == 27:
                        self.process = False
                


if __name__=='__main__':
    parser = argparse.ArgumentParser()              
    parser.add_argument('--input',default=None, type=str, help='path to image.')
    parser.add_argument('--output', default=None, type=str, help='name of output file')
    parser.add_argument('--time', default=None, type=int, help='time in minutes to record')
    parser.add_argument('--fps', default=defaultFPS, type=int, help='frames per second')
    parser.add_argument('--show', default=False, help='show video', action='store_true')
    opt = parser.parse_args()

    VS = VideoSaver(opt)

    p1=threading.Thread(target=VS.Receive, args=())
    p1.start()
    p2 = threading.Thread(target=VS.Display)
    
    p2.start()
    p2.join()
    VS.video_writer.release()
    print("record finidhed")

