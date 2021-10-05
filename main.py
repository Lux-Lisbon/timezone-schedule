# INITIALISATION

import tkinter as tk  # tkinter library, to create gui
from tkinter import ttk
from tkinter import messagebox
import json
import datetime as dt  # datetime library, to import date/time
import pytz  # pytz library, to use timezone format
from geopy.geocoders import Nominatim # geopy library, to get coords from entry
from timezonefinder import TimezoneFinder # timezonefinder library, to get timezone from coords
from replit import db # repl database library, to store info

window = tk.Tk() # initalisation 
window.title("Timezone Program") # to set title of window

import images

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

formEntryList = [
    db["profiles"][0]["name"],
    db["profiles"][0]["business"],
    db["profiles"][0]["timezones"][0], 
    db["profiles"][0]["timezones"][1], 
    db["profiles"][0]["timezones"][2]
]

dataList = []
db["dataList"] = dataList
dbDataList = db["dataList"]

# add profile function 
# find len of profiles and add to db[2] etc

profiles = [
   {
     "name": "Default",
     "business": "Default Business",
     "timezones": ["Australia/Melbourne", "Asia/Singapore", "Italy"]
   },
   {
     "name": "Custom",
     "business": "Custom Business",
     "timezones": ["Australia/Sydney", "Australia/Melbourne", "Australia/Darwin"]
   }
 ]
db["profiles"] = profiles


# variable using tk.StringVar() to dynamically change string
nameVar = tk.StringVar()

# timezoneVars - converting timezoneList elements to a tk.Stringvar
timezoneVar = tk.StringVar()
timezoneVar.set(timezoneList[0])
timezoneVar2 = tk.StringVar()
timezoneVar2.set(timezoneList[1])
timezoneVar3 = tk.StringVar()
timezoneVar3.set(timezoneList[2])

# entry vars
formEntryVar = tk.StringVar()
formEntryVar.set(formEntryList[0])
formEntryVar2 = tk.StringVar()
formEntryVar2.set(formEntryList[1])
formEntryVar3 = tk.StringVar()
formEntryVar3.set(formEntryList[2])
formEntryVar4 = tk.StringVar()
formEntryVar4.set(formEntryList[3])
formEntryVar5 = tk.StringVar()
formEntryVar5.set(formEntryList[4])


def profilePropertyPrinter(formEntry,formEntry2,formEntry3,formEntry4,formEntry5,profileNum):
    try:
        profiles[profileNum]["name"] = printEntry(formEntry)
        profiles[profileNum]["business"] = printEntry(formEntry2)
        profiles[profileNum]["timezones"][0] = printEntry(formEntry3)
        profiles[profileNum]["timezones"][1] = printEntry(formEntry4)
        profiles[profileNum]["timezones"][2] = printEntry(formEntry5)
        # db["profiles"] = profiles
        # print(dat,"\n\n\n",data)
        # keys = db.keys()
        # print(keys)
        
        with open("testprefs.json", 'w', encoding='utf-8') as outputfile:
            json.dump(profiles, outputfile, ensure_ascii=False, indent=4)

    except:
        print("Please Try Again!")
        messagebox.showerror("Error","There was an error in saving your preferences as a JSON file.")

def readAndReturn(jsonFileName):
    with open('{}.json'.format(jsonFileName), 'r') as f:
        data = json.load(f)

    return data

def readAndReplace(profileNum,jsonFileName):
    try:
        with open('{}.json'.format(jsonFileName), 'r') as f:
            data = json.load(f)
        db["data"] = data
        formEntryVar.set(data[profileNum]["name"])
        formEntryVar2.set(data[profileNum]["business"])
        formEntryVar3.set(data[profileNum]["timezones"][0])
        formEntryVar4.set(data[profileNum]["timezones"][1])
        formEntryVar5.set(data[profileNum]["timezones"][2])
    except:
        print("Please Try Again!")
        messagebox.showerror("Error","There was an error in loading your preferences. Please try a different file name!")

def writeReadReplace(formEntry,formEntry2,formEntry3,formEntry4,formEntry5,profileNum,jsonFileName):
    profilePropertyPrinter(formEntry,formEntry2,formEntry3,formEntry4,formEntry5,profileNum)
    readAndReplace(profileNum,jsonFileName)

def createProfileNameList(jsonFileName):
    data = readAndReturn(jsonFileName)
    print(data)
    numOfProfiles = len(data)
    dataList.clear()
    for x in range(numOfProfiles):
        dataList.append(data[x]["name"])
    

createProfileNameList("testprefs")

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
    try:
        # assigns return of given entry
        locationInput = printEntry(entry)
        # applying geocode method to get the location
        locVar = geoLocator.geocode(locationInput, timeout=1000)
        # using .latitude and .latitude methods to get coords of location
        locLat = locVar.latitude
        locLong = locVar.longitude
        return [locLat, locLong]
    except:
        print("Try another location/timezone!")
        messagebox.showerror("Error","Invalid Location/Timezone. Please try another input!")

# getTZ function - converts GPS co-ordinates from getCoords to a timezone for use in clock()
def getTZ(entry, currentTimeZone):
    try:
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
    except:
        print("Try another location/timezone!")
        messagebox.showerror("Error","Invalid Location/Timezone. Please try another input!")

def profileTZSet(timezoneMenu,timezoneMenu2,timezoneMenu3,tz,tz2,tz3,sampleList,num1,num2,num3,nestedCommand):
    try:
        sampleList[num1] = printEntry(timezoneMenu)
        sampleList[num2] = printEntry(timezoneMenu2)
        sampleList[num3] = printEntry(timezoneMenu3)
        timezoneVar.set(sampleList[num1])
        timezoneVar2.set(sampleList[num2])
        timezoneVar3.set(sampleList[num3])
        print(sampleList)
        getTZ(timezoneMenu, tz)
        getTZ(timezoneMenu2, tz2)
        getTZ(timezoneMenu3, tz3)
        createProfileNameList("testprefs")
        try:
            nestedCommand
        except:
            pass
    except:
        print("Try another location/timezone!")
        messagebox.showerror("Error","Invalid Location/Timezone. Please try another input!")

# WIDGETS

# .Frame() and .LabelFrame() - for storing widgets, to organise grid section
content = tk.Frame(window)
content.grid(row=0, column=0, sticky="W,E,S,N")

menuFrame = tk.LabelFrame(content, text="", padx=5, pady=5)
menuFrame.grid(row=0, column=0, sticky="W,E,S,N")

timeFrame = tk.LabelFrame(content, text="", padx=5, pady=5)
timeFrame.grid(row=1, column=0, sticky="W,E,S,N")

mapFrame = tk.LabelFrame(content, text="", padx=5, pady=5)
mapFrame.grid(row=1, column=1, sticky="WESN")

def createNewWindow():
    newWindow = tk.Toplevel(window)

    formHeading = tk.LabelFrame(newWindow, text="Select a Profile", padx=5, pady=5)
    formHeading.grid(row=0, column=0, sticky="W,E,S,N")

    formForm = tk.LabelFrame(newWindow, text="Edit Profile", padx=10, pady=10)
    formForm.grid(row=1, column=0, sticky="W,E,S,N")

    formFooter = tk.LabelFrame(newWindow, text="", padx=10, pady=10)
    formFooter.grid(row=2, column=0, sticky="W,E,S,N")

    def formLabelWrapper(rownum,sampleText,frameVar,colnum):
        formLabel = tk.Label(
              frameVar,
              text=sampleText,
              font=("Arial", 12))
        # packs label to the grid
        formLabel.grid(
              row=rownum,
              column=colnum, 
              sticky="W,E,S,N", 
              pady=10)
        return formLabel

    def formEntryWrapper(rownum,formTextVar):
    # creation and properties of entry widget
        formMenu = tk.Entry(
            formForm,
            textvariable=formTextVar,
            width=25,
            font=("Arial", 12))
        # packs entry field to the grid
        formMenu.grid(
            row=rownum,
            column=2,
            sticky="W,E,S,N",
            padx=5,
            pady=(10))
        return formMenu

    def formApplyButtonWrapper(rownum,colnum,tM,tM2,tM3,tz,tz2,tz3,nestedCommand):
        formButton = tk.Button(
            formFooter,
            text="Apply",
            command=lambda: profileTZSet(tM,tM2,tM3,tz,tz2,tz3,formEntryList,2,3,4,nestedCommand),
            width=15,
            height=2)
        # packs button to the grid
        formButton.grid(
            row=rownum,
            column=colnum,
            sticky="W,E,S,N",
            padx=(5),
            pady=(10, 10))
        return formButton

    ### add pop-up to request json file name for import (currently static as "testprefs")
    def formImportButtonWrapper(rownum,colnum):
        formButton = tk.Button(
            formFooter,
            text="Load Profiles",
            image=images.uploadIcon,
            compound=tk.LEFT,
            command=lambda: readAndReplace(0,"testprefs"),
            width=125,
            height=2)
        # packs button to the grid
        formButton.grid(
            row=rownum,
            column=colnum,
            sticky="W,E,S,N",
            padx=(5),
            pady=(10, 10))
        return formButton

    def formExportButtonWrapper(rownum,colnum,profileNum):
        formButton = tk.Button(
            formFooter,
            text="Save Profiles",
            image=images.downloadIcon,
            compound=tk.LEFT,
            command=lambda: profilePropertyPrinter(formEntry,formEntry2,formEntry3,formEntry4,formEntry5,profileNum),
            width=125,
            height=2)
        # packs button to the grid
        formButton.grid(
            row=rownum,
            column=colnum,
            sticky="W,E,S,N",
            padx=(5),
            pady=(10, 10))
        return formButton   

    testVar = "test342423"

    formDropdown = ttk.OptionMenu(
        formHeading,
        formEntryVar,
        testVar,
        *dataList)
    # formDropdown.config(
    #     width=15)
    #     height=2)
    formDropdown.grid(
        row=0,
        column=0,
        sticky="W,E,S,N",
        padx=(5),
        pady=(10,10))

    def setOptions():
        formDropdown.set_menu(*dataList)
    setOptions = setOptions()

    formLabelWrapper(0,"Name:",formForm,1)
    formLabelWrapper(1,"Business:",formForm,1)
    formLabelWrapper(2,"Timezone 1:",formForm,1)
    formLabelWrapper(3,"Timezone 2:",formForm,1)
    formLabelWrapper(4,"Timezone 3:",formForm,1)
    # formEntry = formEntryWrapper(0,formEntryVar)
    formEntry = formEntryWrapper(0,formEntryVar)
    formEntry2 = formEntryWrapper(1,formEntryVar2)
    formEntry3 = formEntryWrapper(2,formEntryVar3)
    formEntry4 = formEntryWrapper(3,formEntryVar4)
    formEntry5 = formEntryWrapper(4,formEntryVar5)

    # db["profiles"][0]["name"] = printEntry(formEntry)
    # db["profiles"][0]["business"] = printEntry(formEntry2)
    # db["profiles"][0]["timezones"][0] = printEntry(formEntry3)
    # db["profiles"][0]["timezones"][1] = printEntry(formEntry4)
    # db["profiles"][0]["timezones"][2] = printEntry(formEntry5)

    # formEntryWrapper(4,"Enter Timezone 3")
    formApplyButtonWrapper(0,1,formEntry3,formEntry4,formEntry5,"tzVar1","tzVar2","tzVar3",setOptions)
    formImportButtonWrapper(0,2)
    formExportButtonWrapper(0,3,0)


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

# --------------------------------------------------
# Menu Header

def addProfileWrapper(tM,tM2,tM3,tz,tz2,tz3):
    addProfileButton = tk.Button(
        menuFrame,
        text="Set Profile to Default",
        command=lambda: profileTZSet(tM,tM2,tM3,tz,tz2,tz3,timezoneList2,0,1,2),
        width=25,
        height=2)
        # packs button to the grid
    addProfileButton.grid(
        row=0,
        column=1,
        sticky="W,E,S,N",
        padx=5,
        pady=(10,10))

newWindow = tk.Button(
    menuFrame,
    # text="Create New Profile",
    text="Profile Menu",
    image=images.profileIcon,
    compound=tk.LEFT,
    command=lambda: createNewWindow(),
    width=125,
    height=2)
# packs button to the grid
newWindow.grid(
    row=0,
    column=2,
    sticky="S,N",
    padx=5,
    pady=(10,10))

newWindow.photoImage=images.profileIcon

mapLabel = tk.Label(
    mapFrame,
    text="test",
    font=("Arial", 12))
# packs label to the grid
mapLabel.grid(
    row=0,
    column=0, 
    sticky="WESN", 
    pady=10)


# timezoneMenus - entry fields that are used to input timezones for the displayed clocks, used as variables for clock functions below
timezoneMenu = makeTimezoneMenu(1, timezoneVar)
timezoneMenu2 = makeTimezoneMenu(2, timezoneVar2)
timezoneMenu3 = makeTimezoneMenu(3, timezoneVar3)
# print(timezoneMenu,timezoneMenu2,timezoneMenu3)

# run clock functions, creating labels and buttons
clock(makeGuiClockWrapper(makeTimezoneButton(1), 1, "tzVar1", timezoneMenu), "tzVar1")
clock(makeGuiClockWrapper(makeTimezoneButton(2), 2, "tzVar2", timezoneMenu2), "tzVar2")
clock(makeGuiClockWrapper(makeTimezoneButton(3), 3, "tzVar3", timezoneMenu3), "tzVar3")

addProfileWrapper(timezoneMenu, timezoneMenu2, timezoneMenu3, "tzVar1", "tzVar2", "tzVar3")

# used to sort weighting/spacing of rows and columns inside frames
# sort this out
content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=3)
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
timeFrame.rowconfigure(0, weight=1)
timeFrame.rowconfigure(1, weight=1)
timeFrame.rowconfigure(2, weight=1)
timeFrame.rowconfigure(3, weight=1)
timeFrame.columnconfigure(1, weight=1)
timeFrame.columnconfigure(2, weight=2)
newWindow.rowconfigure(0, weight=2)
newWindow.rowconfigure(1, weight=1)
newWindow.rowconfigure(2, weight=1)
newWindow.rowconfigure(3, weight=1)
newWindow.rowconfigure(4, weight=1)
newWindow.columnconfigure(0, weight=1)
newWindow.columnconfigure(1, weight=1)
newWindow.columnconfigure(2, weight=1)


# MAIN LOOP - starts the window
window.mainloop()
