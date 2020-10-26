
import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64
import Source as sc

import cv2
import re
import string

# ------------- Chuyen anh sang .PNG ---------------------------------------------
# (vi o day chi doc duoc image.PNG nen phai chuyen sang.PNG)
def convert_to_bytes(file_or_bytes, resize=None):
   
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

# --------------end ---  Chuyen anh sang .PNG------------------------------------



#-------------- GUI -------------------
# Phần input
input_column = [
 
    [
        sg.Text("Image File"),
        sg.In(size=(39, 1), key='new_image'),
        sg.FileBrowse(target='new_image'),
    
    ],
    [
        sg.Button("Open Image", key='open_image', size=(100, 1)),
        
        
    ],
    [
        sg.Text("Link Image: "),
    
    ],
    [
        sg.Text(size=(50, 3), key="url_image"),
    ],
    [
        sg.Image(key="image_source"),
    ],
    
    # Phần output

    [
        
        sg.Button("Show Result", key='bnt_find'),
        sg.Button("Image Has Been Marked", key='bnt_image_sign'),
        sg.Button("Result Image", key='bnt_image_result'),
        sg.Button("Exit", key='Exit',size=(10, 1)),
    
    ],
    [
        sg.Text("Result: "),
        sg.InputText(size=(50, 1), key="result"),
    ],

 

]


# Full layout 
layout = [
    [
        sg.Column(input_column, justification='center'),
    ]
]

# Layout window GUI
window = sg.Window("LPI 55", layout, size=(450,600)).Finalize()



#---------------------------end GUI-----------------------------------------

#------------ Xoa ky tu thua trong ket qua string -------------------------
def frmstring(s):
    tmp = ""
    for i in s:
        if re.search("[A-Z]",i) or re.search("[0-9]", i):
            tmp += i

    return tmp


#------------ End  Xoa ky tu thua trng ket qua string -------------------------


# ------------------------- event Bnt --------------------------------------------
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # event: click bnt 'open_image'
    if event == "open_image": 
        try:
            # Ten url image
            filename = os.path.join(
                values["new_image"]
            )
            window["url_image"].update(filename)

            # Thay doi kich thuoc image + su dung ham convert_to-bytes ben tren
            new_size = 420, 350
            window["image_source"].update(data=convert_to_bytes(filename, resize=new_size))
        except:
            pass
    # event: click bnt 'bnt-find' , xuat ket qua qua text output
    if event == "bnt_find":
        try:
            # format url C:\\
            filename = os.path.join(
                values["new_image"]
            )
            str_url = filename.replace("/", r"\\")

            # Lay image di xu ly
            img1 = cv2.imread(str_url,cv2.IMREAD_COLOR)
            # Xu ly cat bien so
            Cropped = sc.Xuly(img1, 1)
            # xuat kq text
            text_result = str(sc.Xuat(Cropped))
            tmp = frmstring(text_result)
            window["result"].update(tmp)

        except Exception as E:
            print(f'** Error {E} **')
            pass     
    # bnt_image_sign , xuat anh goc da duoc danh dau bien so
    if event == "bnt_image_sign":
        try:
            # format url C:\\
            filename = os.path.join(
                values["new_image"]
            )
            str_url = filename.replace("/", r"\\")

            # Lay image di xu ly
            img1 = cv2.imread(str_url,cv2.IMREAD_COLOR)

            # danh dau image
            sign = sc.Xuly(img1, 2)
            # goi ham show ben source.py
            sc.image_sign(sign)

        except Exception as E:
            print(f'** Error {E} **')
            pass   
    # image result     , xuat bien so da cat khoi anh goc
    elif event == "bnt_image_result":
        try:
            # format url C:\\
            filename = os.path.join(
                values["new_image"]
            )
            str_url = filename.replace("/", r"\\")

            # Lay image di xu ly
            img1 = cv2.imread(str_url,cv2.IMREAD_COLOR)
            # Xu ly cat bien so
            Cropped = sc.Xuly(img1, 1)
            # xuat kq sau khi cat
            sc.image_crop(Cropped)

        except Exception as E:
            print(f'** Error {E} **')
            pass
# ------------------------ end Event Bnt-----------------------------------



window.close()