# INITIALISATION

import tkinter as tk  # tkinter library, to create gui
import datetime as dt  # datetime library, to import date/time
import pytz  # pytz library, to use timezone format
from geopy.geocoders import Nominatim # geopy library, to get coords from entry
from timezonefinder import TimezoneFinder # timezonefinder library, to get timezone from coords
from replit import db # repl database library, to store info

window = tk.Tk() # initalisation 
window.title("Timezone Program") # to set title of window

# FUNCTIONS

print(db)

# printEntry() function - uses .get() func to retrieve input from (x); an argument defined per use
# assigns input of 'x' (from an entry widget) to 'output' and returns output
def printEntry(x):
    output = x.get()
    return output

# changeText function - uses argument to dynamically change text in a label ('y') to a string ('x')
def changeText(y, x):
    y.set(printEntry(x))

# sample timezones for use in timezoneVar
timezoneList = [
    "Australia/Melbourne", "Singapore", "US/Central", "Europe/Paris"
]

timezoneList2 = [
    "China", "London", "Amsterdam"
]

# add profile function 
# find len of profiles and add to db[2] etc

profiles = [
  {
    "name": "Default",
    "business": "Default Business",
    "groups": ["Australia/Melbourne", "Asia/Singapore"]
  },
  {
    "name": "Custom",
    "business": "Custom Business",
    "groups": ["Australia/Sydney", "Australia/Melbourne"]
  }
]
db["profiles"] = profiles
print(db["profiles"][0]["name"])

# variable using tk.StringVar() to dynamically change string
nameVar = tk.StringVar()

# timezoneVars - converting timezoneList elements to a tk.Stringvar
timezoneVar = tk.StringVar()
timezoneVar.set(timezoneList[0])
timezoneVar2 = tk.StringVar()
timezoneVar2.set(timezoneList[1])
timezoneVar3 = tk.StringVar()
timezoneVar3.set(timezoneList[2])

# creation of custom Nominatim user agent, to avoid violation of usage policy, and HTTP errors
geoLocator = Nominatim(user_agent="tzs_request")

# clock function - clockVar grabs the current time and uses the input of 'y' to convert it to a timezone. nowtime converts that time into a HH:MM:SS format. 
# it then configures the label inputted as argument 'guiClock' to nowTime, and updates every 100ms.
# if something goes wrong, the text will change to "Placeholder", and check every 100ms for changes.
def clock(guiClock, currentTimeZone):
    try:
        clockVar = dt.datetime.now(pytz.timezone(db[currentTimeZone]))
        nowTime = clockVar.strftime("%H:%M:%S\n") + clockVar.strftime("(%A, %d %B %Y)")
        guiClock.config(text=nowTime)
        guiClock.after(100, clock, guiClock, currentTimeZone)

    except:
        print("Clock Except")
        guiClock.after(100, clock, guiClock, currentTimeZone)

# getCoords function - converts text from a given entry into GPS co-ordinates.
def getCoords(entry):
    # assigns return of given entry
    locationInput = printEntry(entry)
    # applying geocode method to get the location
    locVar = geoLocator.geocode(locationInput, timeout=1000)
    # using .latitude and .latitude methods to get coords of location
    locLat = locVar.latitude
    locLong = locVar.longitude
    return [locLat, locLong]

# getTZ function - converts GPS co-ordinates from getCoords to a timezone for use in clock()
def getTZ(entry, currentTimeZone):
    coordsList = getCoords(entry) # assigns the list return from getCoords() to a variable
    tf = TimezoneFinder()
    # imports locLat and locLong from getCoords() through use of the coordsList variable
    locLat = coordsList[0]
    locLong = coordsList[1]
    tzFromCoords = tf.timezone_at(lng=locLong, lat=locLat) # uses timezonefinder library to convert coords to a formatted timezone
    print(tzFromCoords)
    db[currentTimeZone] = tzFromCoords # stores timezone in a repl database, for use in clocks
    print(currentTimeZone, db[currentTimeZone])
    return tzFromCoords

def profileTZSet(value1,value2,value3,timezoneMenu,timezoneMenu2,timezoneMenu3,tz,tz2,tz3):
    # db["tzVar1"] = value1
    # db["tzVar2"] = value2
    # db["tzVar3"] = value3
    timezoneVar.set(timezoneList2[0])
    timezoneVar2.set(timezoneList2[1])
    timezoneVar3.set(timezoneList2[2])
    getTZ(timezoneMenu, tz)
    getTZ(timezoneMenu2, tz2)
    getTZ(timezoneMenu3, tz3)



# WIDGETS

# .Frame() and .LabelFrame() - for storing widgets, to organise grid section
content = tk.Frame(window)
content.grid(sticky="W,E,S,N")

menuFrame = tk.LabelFrame(content, text="", padx=5, pady=5)
menuFrame.grid(row=0, column=0, sticky="W,E,S,N")

timeFrame = tk.LabelFrame(content, text="", padx=5, pady=5)
timeFrame.grid(row=1, column=0, sticky="W,E,S,N")

# textFrame = tk.LabelFrame(content, text="", padx=5, pady=5)
# textFrame.grid(row=0, column=1, sticky="W,E,S,N")

# makeTimezoneMenu creates a tkinter entry field widget with customisable text variables and row numbers
def makeTimezoneMenu(rownum, timezoneVar):
    # creation and properties of entry widget
    timezoneMenu = tk.Entry(
        timeFrame,
        textvariable=timezoneVar,
        width=25,
        font=("Arial", 12))
    # packs entry field to the grid
    timezoneMenu.grid(
        row=rownum,
        column=1,
        sticky="W,E,S,N",
        padx=5,
        pady=(2, 70))
    return timezoneMenu

# makeTimezoneButton creates a tkinter button widget, with an argument for a customisable row number.
def makeTimezoneButton(rownum):
    # creation and properties of button widget
    timezoneButton = tk.Button(
        timeFrame,
        text="Submit",
        command="",
        width=25,
        height=2)
    # packs button to the grid
    timezoneButton.grid(
        row=rownum,
        column=1,
        sticky="W,E,S,N",
        padx=(5),
        pady=(70, 10))
    return timezoneButton

# makeGuiClockWrapper creates a tkinter label widget with arguments for a row number.
def makeGuiClockWrapper(tzButton, rownum, tz, timezoneMenu):
    # creation and properties of label widget
    guiClock = tk.Label(
        timeFrame,
        text="",
        bg="black",
        fg="white",
        width=30,
        height=5,
        font=("Arial", 14))
    # packs label to the grid
    guiClock.grid(
        row=rownum,
        column=2, 
        sticky="W,E,S,N", 
        pady=2)
    # sets button command to change a clock's timezone based on the input of a given entry field
    tzButton.config(command=lambda: getTZ(timezoneMenu, tz))
    return guiClock

def addProfileWrapper(tM,tM2,tM3,tz,tz2,tz3):
    addProfileButton = tk.Button(
        menuFrame,
        text="Set Profile",
        command=lambda: profileTZSet(timezoneList2[0],timezoneList2[1],timezoneList2[2],tM,tM2,tM3,tz,tz2,tz3),
        width=25,
        height=2
      )
        # packs button to the grid
    addProfileButton.grid(
        row=0,
        column=1,
        sticky="W,E,S,N",
        padx=(5),
        pady=(10, 10)
      )


# timezoneMenus - entry fields that are used to input timezones for the displayed clocks, used as variables for clock functions below
timezoneMenu = makeTimezoneMenu(1, timezoneVar)
timezoneMenu2 = makeTimezoneMenu(2, timezoneVar2)
timezoneMenu3 = makeTimezoneMenu(3, timezoneVar3)

# used to sort weighting/spacing of rows and columns inside frames
content.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
timeFrame.rowconfigure(0, weight=1)
timeFrame.rowconfigure(1, weight=1)
timeFrame.rowconfigure(2, weight=1)
timeFrame.rowconfigure(3, weight=1)
timeFrame.columnconfigure(1, weight=1)
timeFrame.columnconfigure(2, weight=2)

# run clock functions, creating labels and buttons
clock(makeGuiClockWrapper(makeTimezoneButton(1), 1, "tzVar1", timezoneMenu), "tzVar1")
clock(makeGuiClockWrapper(makeTimezoneButton(2), 2, "tzVar2", timezoneMenu2), "tzVar2")
clock(makeGuiClockWrapper(makeTimezoneButton(3), 3, "tzVar3", timezoneMenu3), "tzVar3")

addProfileWrapper(timezoneMenu, timezoneMenu2, timezoneMenu3, "tzVar1", "tzVar2", "tzVar3")

# MAIN LOOP - starts the window
window.mainloop()
