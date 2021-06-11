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
from replit import db


window = tk.Tk()
window.title("Timezone Program")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# FUNCTIONS


print("nooooo waaayyyyyy")

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

geoLocator = Nominatim(user_agent="tzs_request")

def clockButtonPress(y,text):
    clockButtonPress.timezoneRetriever = getTZ(y)
    guiClock.config(text=text)
    # guiClock.after(100, clock, y, guiClock, button)


def clock(guiClock,currentTimeZone):
    #global currentTimezone
    #currentTimeZone = "Europe/Paris"
    try:
        # clockButtonPress(y,varTemp2)
        #tz = getTZ(entryWidget)
        #print("currentTimeZone2", currentTimeZone)
        #clockVar = dt.datetime.now(pytz.timezone(ct))
        clockVar = dt.datetime.now(pytz.timezone(db[currentTimeZone]))
        nowTime = clockVar.strftime("%H:%M:%S")
        
        # guiClock.after(100, clock, y, guiClock, button)
        #print("here???", nowTime)
        guiClock.config(text=nowTime)
        #print("!!!")
        guiClock.after(100, clock, guiClock, currentTimeZone)
    
    except:
        print("exepppt")
        guiClock.after(100, clock, guiClock, currentTimeZone)
        #guiClock.after(100, clock, y, guiClock, button)


# set variable to return input from timezoneMenu entry
# locationInput = printEntry(timezoneMenu)

def getCoords(entry):
    # assigns return of given entry
    locationInput = printEntry(entry)
    # applying geocode method to get the location
    locVar = geoLocator.geocode(locationInput, timeout=1000)
    #print(locVar)
    # using .latitude and .latitude methods to get coords of location
    locLat = locVar.latitude
    locLong = locVar.longitude
    #print(locLat)
    #print(locLong)
    return [locLat, locLong]

def getTZ(entry,currentTimeZone):
    coordsList = getCoords(entry)
    tf = TimezoneFinder()
    locLat = coordsList[0]
    locLong = coordsList[1]
    tzFromCoords = tf.timezone_at(lng=locLong, lat=locLat)
    print(tzFromCoords)
    #currentTimeZone = tzFromCoords
    db[currentTimeZone] = tzFromCoords
    print("currentTimeZone1", db["currentTimeZone"])
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
def makeTimezoneMenu(rownum,timezoneVar):
  timezoneMenu = tk.Entry(
      timeFrame,
      textvariable=timezoneVar,
      width=25,
      font=("Arial", 12)
    )
  timezoneMenu.grid(row=rownum,column=1,sticky="W,E,S,N",padx=5,pady=(2,70))
  return timezoneMenu

def makeTimezoneButton(rownum):
  timezoneButton = tk.Button(
      timeFrame,
      text="Submit",
      command="",
      width=25,
      height=2
    )
  timezoneButton.grid(row=rownum,column=1,sticky="W,E,S,N",padx=(5),pady=(70,10))
  return timezoneButton

def makeGuiClockWrapper(tzButton, rownum, tz, timezoneMenu):
  guiClock = tk.Label(
      timeFrame,
      text="",
      bg="black",
      fg="white",
      width=30,
      height=5,
      font=("Arial", 14)
      )
  guiClock.grid(row=rownum,column=2,sticky="W,E,S,N",pady=2)
  tzButton.config(command=lambda: getTZ(timezoneMenu,tz))
  return guiClock

timezoneMenu = makeTimezoneMenu(0,timezoneVar)
timezoneMenu2 = makeTimezoneMenu(1,timezoneVar2)
# used to sort weighting/spacing of rows and columns inside frames
timeFrame.rowconfigure(0,weight=1)
timeFrame.rowconfigure(1,weight=1)
timeFrame.rowconfigure(2,weight=1)
timeFrame.rowconfigure(3,weight=1)
timeFrame.columnconfigure(1, weight=1)
timeFrame.columnconfigure(2, weight=2)


clock(makeGuiClockWrapper(makeTimezoneButton(0),0,"tzVar1",timezoneMenu), "tzVar1")
clock(makeGuiClockWrapper(makeTimezoneButton(1),1,"tzVar2",timezoneMenu2), "tzVar2")

# MAIN LOOP - starts the window
window.mainloop()
