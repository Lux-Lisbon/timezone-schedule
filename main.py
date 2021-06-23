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

# variable using tk.StringVar() to dynamically change string
nameVar = tk.StringVar()

# timezoneVars - converting timezoneList elements to a tk.Stringvar
timezoneVar = tk.StringVar()
timezoneVar.set(timezoneList[0])
timezoneVar2 = tk.StringVar()
timezoneVar2.set(timezoneList[1])

# creation of custom Nominatim user agent, to avoid violation of usage policy, and HTTP errors
geoLocator = Nominatim(user_agent="tzs_request")

# clock function - clockVar grabs the current time and uses the input of 'y' to convert it to a timezone. nowtime converts that time into a HH:MM:SS format. 
# it then configures the label inputted as argument 'guiClock' to nowTime, and updates every 100ms.
# if something goes wrong, the text will change to "Placeholder", and check every 100ms for changes.
def clock(guiClock, currentTimeZone):
    try:
        clockVar = dt.datetime.now(pytz.timezone(db[currentTimeZone]))
        nowTime = clockVar.strftime("%H:%M:%S")
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
    print("currentTimeZone1", db["currentTimeZone"])
    return tzFromCoords

# WIDGETS

# .Frame() and .LabelFrame() - for storing widgets, to organise grid section
content = tk.Frame(window)
content.grid()

timeFrame = tk.LabelFrame(content, text="", padx=5, pady=5)
timeFrame.grid(row=0, column=0, sticky="W,E,S,N")

textFrame = tk.LabelFrame(content, text="", padx=5, pady=5)
textFrame.grid(row=0, column=1, sticky="W,E,S,N")

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

# timezoneMenus - entry fields that are used to input timezones for the displayed clocks, used as variables for clock functions below
timezoneMenu = makeTimezoneMenu(0, timezoneVar)
timezoneMenu2 = makeTimezoneMenu(1, timezoneVar2)

# used to sort weighting/spacing of rows and columns inside frames
timeFrame.rowconfigure(0, weight=1)
timeFrame.rowconfigure(1, weight=1)
timeFrame.rowconfigure(2, weight=1)
timeFrame.rowconfigure(3, weight=1)
timeFrame.columnconfigure(1, weight=1)
timeFrame.columnconfigure(2, weight=2)

# run clock functions, creating labels and buttons
clock(makeGuiClockWrapper(makeTimezoneButton(0), 0, "tzVar1", timezoneMenu), "tzVar1")
clock(makeGuiClockWrapper(makeTimezoneButton(1), 1, "tzVar2", timezoneMenu2), "tzVar2")

# MAIN LOOP - starts the window
window.mainloop()
