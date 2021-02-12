#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# INITIALISATION


# tkinter library, to create gui
# datetime library, to import date/time
import tkinter as tk
from tkinter import ttk
import ttkwidgets
from ttkwidgets import autocomplete
import datetime as dt
import time
import pytz
import geopy
import timezonefinder

# Tk() initialises a tkinter window
window = tk.Tk()
# .title() sets the title of the gui
window.title("Timezone Program")
# window.geometry("1920x1080")


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# FUNCTIONS


# printEntry() function - uses .get() func to retrieve input from (x); an argument defined per use
# assigns input of 'x' (from an entry widget) to 'output' and returns output
def printEntry(x):
    output = x.get()
    return output

timezoneList = [
    "Australia/Melbourne",
    "Singapore",
    "US/Central",
    "Europe/Paris"
]

# variable using tk.StringVar() to dynamically change string
nameVar = tk.StringVar()

timezoneVar = tk.StringVar()
timezoneVar.set(timezoneList[0])

timezoneVar2 = tk.StringVar()
timezoneVar2.set(timezoneList[1])

timezoneVar3 = tk.StringVar()
timezoneVar3.set(timezoneList[2])

timezoneVar4 = tk.StringVar()
timezoneVar4.set(timezoneList[3])

# changeText function - uses argument to dynamically change text in a label using the above 'printEntry' function and 'nameEntry' var
def changeText(y,x):
    y.set(printEntry(x)) 

# def selected(event):


def clock(y):
    try:
        clockVar = dt.datetime.now(pytz.timezone(y.get()))
        nowTime = clockVar.strftime("%H:%M:%S")

        # guiClock.config(text=timezoneVar.get())
        guiClock.config(text=nowTime)
        guiClock.after(1000, clock, y)
    
    except:
        guiClock.config(text="Placeholder")
        guiClock.after(1000, clock, y)

def clock2(timezoneMenu2):
    # nowTime2 = dt.datetime.now(timeSingapore)
    try:
        clockVar2 = dt.datetime.now(pytz.timezone(timezoneMenu2.get()))
        nowTime2 = clockVar2.strftime("%H:%M:%S")

        guiClock2.config(text=nowTime2)
        guiClock2.after(1000, clock2)
    
    except:
        guiClock2.config(text="Placeholder 2")

def clock3(timezoneMenu3):
    try:   
        clockVar3 = dt.datetime.now(pytz.timezone(timezoneMenu3.get()))
        nowTime3 = clockVar3.strftime("%H:%M:%S")

        guiClock3.config(text=nowTime3)
        guiClock3.after(1000, clock3)

    except:
        guiClock3.config(text="Placeholder 3")

def clock4(timezoneMenu4):
    try:
        clockVar4 = dt.datetime.now(pytz.timezone(timezoneMenu4.get()))
        nowTime4 = clockVar4.strftime("%H:%M:%S")

        guiClock4.config(text=nowTime4)
        guiClock4.after(1000, clock4)

    except:
        guiClock4.config(text="Placeholder 4")


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# WIDGET SECTION - LABELS, ENTRY AND BUTTON

content = tk.Frame(
    window
)
content.grid()

timeFrame = tk.LabelFrame(
    content,
    text="",
    padx=5,
    pady=5
)
timeFrame.grid(row=0,column=0,sticky="W,E,S,N")

textFrame = tk.LabelFrame(
    content,
    text="",
    padx=5,
    pady=5
)
textFrame.grid(row=0,column=1,sticky="W,E,S,N")

timezoneMenu = tk.Entry(
    timeFrame,
    textvariable=timezoneVar,
    width=25,
    font=("Arial", 12)
)
timezoneMenu.grid(row=0,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))

timezoneMenu2 = tk.Entry(
    timeFrame,
    width=25,
    font=("Arial", 12)
)
timezoneMenu2.grid(row=1,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))

timezoneMenu3 = tk.Entry(
    timeFrame,
    width=25,
    font=("Arial", 12)
)
timezoneMenu3.grid(row=2,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))

timezoneMenu4 = tk.Entry(
    timeFrame,
    width=25,
    font=("Arial", 12)
)
timezoneMenu4.grid(row=3,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))

timezoneButton = tk.Button(
    timeFrame,
    text="Submit",
    # command=lambda: print(printEntry(nameEntry)),
    command=lambda: changeText(timezoneVar,timezoneMenu),
    width=25,
    height=2
    )
timezoneButton.grid(row=0,column=1,sticky="W,E,S,N",padx=(5),pady=(70,10)) # .pack() required to add button

timezoneButton2 = tk.Button(
    timeFrame,
    text="Submit",
    # command=lambda: print(printEntry(nameEntry)),
    command=lambda: changeText(timezoneVar2,timezoneMenu2),
    width=25,
    height=2
    )
timezoneButton2.grid(row=1,column=1,sticky="W,E,S,N",padx=(5),pady=(70,10)) # .pack() required to add button

timezoneButton3 = tk.Button(
    timeFrame,
    text="Submit",
    # command=lambda: print(printEntry(nameEntry)),
    command=lambda: changeText(timezoneVar3,timezoneMenu3),
    width=25,
    height=2
    )
timezoneButton3.grid(row=2,column=1,sticky="W,E,S,N",padx=(5),pady=(70,10)) # .pack() required to add button

timezoneButton4 = tk.Button(
    timeFrame,
    text="Submit",
    # command=lambda: print(printEntry(nameEntry)),
    command=lambda: changeText(timezoneVar4,timezoneMenu4),
    width=25,
    height=2
    )
timezoneButton4.grid(row=3,column=1,sticky="W,E,S,N",padx=(5),pady=(70,10)) # .pack() required to add button

# tk.Label() - used to add text
guiClock = tk.Label(
    timeFrame,
    # textvariable=timezoneVar,
    text="",
    bg="black",
    fg="white",
    width=30,
    height=5,
    font=("Arial", 14)
    )
guiClock.grid(row=0,column=2,sticky="W,E,S,N",pady=2)
# guiClock.pack() # .pack() required to add label
clock(timezoneMenu)

guiClock2 = tk.Label(
    timeFrame,
    text="",
    bg="black",
    fg="white",
    width=30,
    height=5,
    font=("Arial", 14)
    )
guiClock2.grid(row=1,column=2,sticky="W,E,S,N",pady=2) # .pack() required to add label
clock2(timezoneMenu2)

guiClock3 = tk.Label(
    timeFrame,
    text="",
    bg="black",
    fg="white",
    width=30,
    height=5,
    font=("Arial", 14)
    )
guiClock3.grid(row=2,column=2,sticky="W,E,S,N",pady=2) # .pack() required to add label
clock3(timezoneMenu3)

guiClock4 = tk.Label(
    timeFrame,
    text="",
    bg="black",
    fg="white",
    width=30,
    height=5,
    font=("Arial", 14)
    )
guiClock4.grid(row=3,column=2,sticky="W,E,S,N",pady=2) # .pack() required to add label
clock4(timezoneMenu4)


# tk.Label() - used to add text
namePrompt = tk.Label(
    textFrame,
    text="Please enter your name below.",
    width=32,
    font=("Arial", 14)
    )
namePrompt.grid(row=0,column=3,sticky="W,E,S,N",pady=2) # .pack() required to add label


# tk.Entry() - used to let user input data
nameEntry = tk.Entry(
    textFrame,
    width=25,
    font=("Arial", 12)
    )
nameEntry.grid(row=1,column=3,sticky="W,E,S,N",pady=(0,80),padx=(10)) # .pack() required to add entry


# tk.Button() - used to add a clickable button
button = tk.Button(
    textFrame,
    text="Submit",
    # command=lambda: print(printEntry(nameEntry)),
    command=lambda: changeText(nameVar,nameEntry),
    width=25,
    height=2
    )
button.grid(row=1,column=3,sticky="W,E,S,N",pady=(60,0),padx=(10)) # .pack() required to add button


# tk.Label() - used to add text
greet = tk.Label(
    textFrame,
    textvariable=nameVar,
    bg="black", 
    fg="white",
    width=30,
    height=15,
    font=("Arial", 14)
    )
greet.grid(row=2,column=3,sticky="W,E,S,N",pady=(10,0))
# greet.pack() # .pack() required to add label

timeFrame.rowconfigure(0,weight=1)
timeFrame.rowconfigure(1,weight=1)
timeFrame.rowconfigure(2,weight=1)
timeFrame.rowconfigure(3,weight=1)
timeFrame.columnconfigure(1, weight=1)
timeFrame.columnconfigure(2, weight=2)
# MAIN LOOP - starts the window
window.mainloop()