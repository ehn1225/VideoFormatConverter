import cv2 as cv
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox 
import tkinter.filedialog
import os

video_file = ""
target_format = ""
codec = ""
frame = Tk()
frame.geometry("400x300")
frame.title("VideoFormatConverter")
frame.option_add("*Font","맑은고딕 15")
frame.resizable(False, False)

def StartEncoding():
    global target_format
    global video_file
    global codec
    target_format = combo_format.get()
    codec = combo_encode.get()

    label_status.config(text="변환 중\n")
    frame.update_idletasks() 

    video = cv.VideoCapture(video_file)
    if video.isOpened():
        target = cv.VideoWriter()
        while True:
            valid, img = video.read()
            if not valid:
                break

            if not target.isOpened():
                filename = os.path.basename(video_file)
                target_file = filename[:filename.rfind('.')] + '.' + target_format
                fps = video.get(cv.CAP_PROP_FPS)
                h, w, *_ = img.shape
                is_color = (img.ndim > 2) and (img.shape[2] > 1)
                target.open(target_file, cv.VideoWriter_fourcc(*(codec)), fps, (w, h), is_color)

            target.write(img)

        target.release()
        label_status.config(text="변환 완료")
        tkinter.messagebox.showinfo(title="비디오 변환 완료", message=f'파일명 : {target_file}\n프레임 : {fps}\n확장자 : {target_format}\n코덱 : {codec}')

def SelectFile():
    global video_file
    video_file = tkinter.filedialog.askopenfilename()
    label_status.config(text="변환 대기")
def SelectCodec():
    global codec
    codec = combo_format.get()

btn_start = Button(frame)
btn_start.config(text="변환할 파일 선택")
btn_start.config(width=20)
btn_start.config(command=SelectFile)
btn_start.pack()

formatList=["avi", "mp4", "wmv", "mov"]
combo_format = ttk.Combobox(frame)
combo_format.config(height=5)
combo_format.config(values=formatList)
combo_format.config(state="readonly")
combo_format.set("확장자선택")
combo_format.pack()

encode_list=['MJPG', 'DIVX', 'H264', 'XVID']
combo_encode = ttk.Combobox(frame)
combo_encode.config(height=5)
combo_encode.config(values=encode_list)
combo_encode.config(state="readonly")
combo_encode.set("코덱 선택")
combo_encode.pack()  

btn_start = Button(frame)
btn_start.config(text="변환 시작")
btn_start.config(width=20)
btn_start.config(command=StartEncoding)
btn_start.pack()

label_status = Label(frame)
label_status.pack()

label_status.config(text="변환 대기")
frame.mainloop()
