import tkinter as tk
import tkinter.ttk
from PIL import Image
from PIL import ImageTk

def imageDefine(location):
    img = Image.open("{}".format(location))
    img = img.resize((25,25), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    return photo
# Creating a photoimage object to use image

profileIcon = imageDefine("imageFolder/profile.png")
uploadIcon = imageDefine("imageFolder/upload.png")
downloadIcon = imageDefine("imageFolder/download.png")
checkIcon = imageDefine("imageFolder/check.png")
undoIcon = imageDefine("imageFolder/undo.png")
mapIcon = imageDefine("imageFolder/map.png")