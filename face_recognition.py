from asyncio import subprocess
from re import L
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import webbrowser
from PIL import Image,ImageTk
from matplotlib.pyplot import gray, text, title
import numpy as np
import os
import cv2
import sqlite3
from datetime import datetime
from time import strftime
class Face_recognition:
    def __init__(self,root):                                     
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("face recognition system")
        title_lbl=Label(self.root,text="FACE RECOGNITION",font=("times new roman",38,"bold"),bg="white",fg="GREEN")
        title_lbl.place(x=0,y=0,width=1530,height=45)
        
        img_top =Image.open(r'face_detection_attendance_system_full_project/college_images/c.jpg')
        img_top=img_top.resize((650,700),Image.ANTIALIAS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        self.photoimg_top=ImageTk.PhotoImage(img_top)
        
        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=650,height=700)
        
        img_bottom =Image.open(r'face_detection_attendance_system_full_project/college_images/c.jpg')
        img_bottom=img_bottom.resize((950,700),Image.ANTIALIAS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)
        
        f_lbl=Label(self.root,image=self.photoimg_bottom)
        f_lbl.place(x=650,y=55,width=950,height=700)

        b1_1=Button(f_lbl,text="Face Recognition",command=self.face_recog,cursor="hand2",font=("times new roman",18,"bold"),bg="darkblue",fg="red")
        b1_1.place(x=350,y=620,width=250,height=40)
    
    def mark_attendance(self,i,d):
        path="/home/astirmind/face_detection_attendance_system_full_project/save.csv"
        with open(path,"r+",newline="\n") as f:
            mydatalist=f.readlines()
            name_list=[]
            for line in mydatalist:
                entry=line.split((","))
                name_list.append(entry[0])
            if ((i not in name_list)) and ((d not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtstring=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{d},{dtstring},{d1},Present")
            else:
                pass
    
    
    
    
    def face_recog(self):
        def draw_boundary(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)
            coord=[]
            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300)))
                con = sqlite3.connect("studentnew.db")
                cur = con.cursor()
                # cur.execute("select id from student where id=" + str(id))
                # n=cur.fetchone()
                # n="+".join(n)
                cur.execute("select name from student where id=" + str(id))
                i=cur.fetchone()
                #
                i=str(i)
                i="+".join(i)
                cur.execute("select gender from student where id=" + str(id))
                d=cur.fetchone()
                d=str(d)
                d="+".join(d)
                
                if confidence>77:
                    # cv2.putText(img,f"id:{n}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"name:{i}",(x,y-35),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"gender:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,d)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                coord=[x,y,w,h] 
            return coord   
        def recognize(img,clf,faceCascade):
            coord=draw_boundary(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
            return img
        faceCascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        # clf.load("classifier.xml")
        video_cap=cv2.VideoCapture(0)
        while True:
            ret,img=video_cap.read()
            img=recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to Face Recognition",img)
            if cv2.waitKey(1)==13:
                break
        video_cap.release()
        cv2.destroyAllWindows()
                    
if __name__=="__main__":
    root=Tk()
    obj=Face_recognition(root)
    root.mainloop()    