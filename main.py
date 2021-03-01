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
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

# Tk() initialises a tkinter window
window = tk.Tk()
# .title() sets the title of the gui
window.title("Timezone Program")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# FUNCTIONS


# printEntry() function - uses .get() func to retrieve input from (x); an argument defined per use
# assigns input of 'x' (from an entry widget) to 'output' and returns output
def printEntry(x):
    output = x.get()
    return output

# changeText function - uses argument to dynamically change text in a label ('y') to a string ('x')
def changeText(y,x):
    y.set(printEntry(x)) 

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

geoLocator = Nominatim(user_agent="tzs_request")

# clock function - clockVar grabs the current time and uses the input of 'y' to convert it to a timezone. nowtime converts that time into a HH:MM:SS format. 
# it then configures the label inputted as argument 'guiClock' to nowTime, and updates every 100ms.
# if something goes wrong, the text will change to "Placeholder", and check every 100ms for changes.
def clock(y,guiClock,tz):
    try:
        varTemp = getTZ(y)
        clockVar = dt.datetime.now(pytz.timezone(varTemp))
        nowTime = clockVar.strftime("%H:%M:%S")

        # guiClock.config(text=timezoneVar.get())
        guiClock.config(text=nowTime)
        # print("hello")
        guiClock.after(100, clock, y, guiClock, tz)
    
    except:
        guiClock.config(text="Placeholder")
        guiClock.after(100, clock, y, guiClock, tz)

# set variable to return input from timezoneMenu entry
# locationInput = printEntry(timezoneMenu)

def getCoords(entry):
    # assigns return of given entry
    locationInput = printEntry(entry)
    # applying geocode method to get the location
    locVar = geoLocator.geocode(locationInput, timeout=1000)
    print(locVar)
    # using .latitude and .latitude methods to get coords of location
    locLat = locVar.latitude
    locLong = locVar.longitude
    print(locLat)
    print(locLong)
    return [locLat, locLong]

def getTZ(entry):
    coordsList = getCoords(entry)
    tf = TimezoneFinder()
    locLat = coordsList[0]
    locLong = coordsList[1]
    tzFromCoords = tf.timezone_at(lng=locLong, lat=locLat)
    print(tzFromCoords)
    return tzFromCoords


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# WIDGET SECTION

# .Frame() and .LabelFrame() - for storing widgets, to organise grid section
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

# timezoneMenus - entry fields that are used to input timezones for the displayed clocks
timezoneMenu = tk.Entry(
    timeFrame,
    textvariable=timezoneVar,
    width=25,
    font=("Arial", 12)
)
timezoneMenu.grid(row=0,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))
# getTZ(timezoneMenu)

timezoneMenu2 = tk.Entry(
    timeFrame,
    textvariable=timezoneVar2,
    width=25,
    font=("Arial", 12)
)
timezoneMenu2.grid(row=1,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))

timezoneMenu3 = tk.Entry(
    timeFrame,
    textvariable=timezoneVar3,
    width=25,
    font=("Arial", 12)
)
timezoneMenu3.grid(row=2,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))

timezoneMenu4 = tk.Entry(
    timeFrame,
    textvariable=timezoneVar4,
    width=25,
    font=("Arial", 12)
)
timezoneMenu4.grid(row=3,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))

# timezoneButtons - buttons to submit entries in timezoneMenu fields. command changes the text of a label to input found in timezoneMenu
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

# guiClocks - labels that display the given clock() function below to display time converted to a timezone given from timezoneMenu fields
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
# tz = getTZ(timezoneMenu)
clock(timezoneMenu, guiClock, getTZ(timezoneMenu))

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
# clock(timezoneMenu2, guiClock2)

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
# clock(timezoneMenu3, guiClock3)

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
# clock(timezoneMenu4, guiClock4)


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

# used to sort weighting/spacing of rows and columns inside frames
timeFrame.rowconfigure(0,weight=1)
timeFrame.rowconfigure(1,weight=1)
timeFrame.rowconfigure(2,weight=1)
timeFrame.rowconfigure(3,weight=1)
timeFrame.columnconfigure(1, weight=1)
timeFrame.columnconfigure(2, weight=2)
# MAIN LOOP - starts the window
window.mainloop()