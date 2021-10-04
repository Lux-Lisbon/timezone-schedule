import tkinter as tk
import tkinter.ttk
from PIL import Image
from PIL import ImageTk

# Creating a photoimage object to use image
img = Image.open("profile.png")
img = img.resize((25,25), Image.ANTIALIAS)
profilesPhoto = ImageTk.PhotoImage(img)