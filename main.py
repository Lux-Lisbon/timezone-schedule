# INITIALISATION

import tkinter as tk  # tkinter library, to create gui
from tkinter import ttk # import ttk from tkinter, an extension 
from tkinter import messagebox # import messagebox from tkinter, a messagebox exception to display except: notices
import gmplot # to plot coordinates on a google map
import flask # flask library, to create a virtual web server
import gmplotTest # gmplotTest.py, another file within this folder
import json # json language for storing/saving/writing/editing profiles
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

# sample timezone for use in profile form
timezoneList2 = [
    "China", "London", "Amsterdam"
]

# list of database stores for conversion to tk.stringvar
formEntryList = [
    db["profiles"][0]["name"],
    db["profiles"][0]["business"],
    db["profiles"][0]["timezones"][0], 
    db["profiles"][0]["timezones"][1], 
    db["profiles"][0]["timezones"][2]
]

# another list of database stores for conversion to tk.stringvar under a different name - as required
formProfileList = [
    "",
    db["profiles"][0]["name"],
    db["profiles"][0]["business"],
    db["profiles"][0]["timezones"][0], 
    db["profiles"][0]["timezones"][1], 
    db["profiles"][0]["timezones"][2]
]

# creation of datalist list and database key for use in dropdown menu
dataList = []
db["dataList"] = dataList
dbDataList = db["dataList"]

# add profile function 
# find len of profiles and add to db[2] etc

# profiles dictionary for default template of what profile json should look like
# this profiles dictionary is written as a template when writing to json
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
formProfileVar = tk.StringVar()
formProfileVar.set(formProfileList[1])

# the profilePropertyPrinter() function is used to save profile preferences/inputs
# a.k.a writing the profile preferences/inputs to (in this case) testPrefs.json
# takes arguments formEntry,formEntry2 (inputs of form entry fields) etc... and writes them to the JSON file.
# try/except is implemented to catch any errors. if except runs, a message box will appear on screen.
def profilePropertyPrinter(formEntry,formEntry2,formEntry3,formEntry4,formEntry5,profileNum):
    try:
        profiles[profileNum]["name"] = printEntry(formEntry)
        profiles[profileNum]["business"] = printEntry(formEntry2)
        profiles[profileNum]["timezones"][0] = printEntry(formEntry3)
        profiles[profileNum]["timezones"][1] = printEntry(formEntry4)
        profiles[profileNum]["timezones"][2] = printEntry(formEntry5)
        
        with open("testprefs.json", 'w', encoding='utf-8') as outputfile:
            json.dump(profiles, outputfile, ensure_ascii=False, indent=4)

    except:
        print("Please Try Again!")
        messagebox.showerror("Error","There was an error in saving your preferences as a JSON file.")

# the readAndReturn() function is used to load profile preferences/inputs from a JSON file as defined in an argument.
# the functions only loads the JSON, and then returns it as a dictionary.
def readAndReturn(jsonFileName):
    with open('{}.json'.format(jsonFileName), 'r') as f:
        data = json.load(f)

    return data

# the readAndReturn() function is used to load profile preferences/inputs from a JSON file as defined in an argument.
# on top of viewing the loaded JSON, it REPLACES the current inputs with the ones stored from the JSON, therefore "loading".
# this is unlike readAndReturn(), which merely views the JSON and returns it as a dictionary.
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

# the createProfileNameList() function is used to create the list of profile names shown in the dropdown menu.
def createProfileNameList(jsonFileName):
    data = readAndReturn(jsonFileName)
    print(data)
    numOfProfiles = len(data)
    dataList.clear()
    dataList.append("")
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

# the profileTZSet() function is responsible for applying the preferences of the selected profile to the timezones in the main window. if this fails, an error messagebox will appear.
def profileTZSet(timezoneMenu,timezoneMenu2,timezoneMenu3,tz,tz2,tz3,sampleList,num1,num2,num3,nestedCommand):
    try:
        # tries assigning user inputs currently in main program to sampleList[]
        sampleList[num1] = printEntry(timezoneMenu)
        sampleList[num2] = printEntry(timezoneMenu2)
        sampleList[num3] = printEntry(timezoneMenu3)
        # sets StringVars to those user inputs
        timezoneVar.set(sampleList[num1])
        timezoneVar2.set(sampleList[num2])
        timezoneVar3.set(sampleList[num3])
        # sets the coordinates of each clock to the inputs from the forms using the database
        getTZ(timezoneMenu, tz)
        getTZ(timezoneMenu2, tz2)
        getTZ(timezoneMenu3, tz3)
        # updates the list of profiles within the dropdown list
        createProfileNameList("testprefs")
        formProfileVar.set(formProfileList[1])
        try:
            nestedCommand
            print("test")
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

# the createNewWindow() function is responsible for everything that regards the GUI of the 'Profile Menu'
def createNewWindow():
    # .Frame() and .LabelFrame() - for storing widgets, to organise grid section
    newWindow = tk.Toplevel(window)
    formHeading = tk.LabelFrame(newWindow, text="Select a Profile", padx=5, pady=5)
    formHeading.grid(row=0, column=0, sticky="W,E,S,N")
    formForm = tk.LabelFrame(newWindow, text="Edit Profile", padx=10, pady=10)
    formForm.grid(row=1, column=0, sticky="W,E,S,N")
    formFooter = tk.LabelFrame(newWindow, text="", padx=10, pady=10)
    formFooter.grid(row=2, column=0, sticky="W,E,S,N")

    # the formLabelWrapper() function creates the text widgets on-screen.
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

    # the formEntryWrapper() function creates the entry fields on-screen.
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

    # the formApplyButtonWrapper() function creates the apply button within the profile menu.
    def formApplyButtonWrapper(rownum,colnum,tM,tM2,tM3,tz,tz2,tz3,nestedCommand):
        formButton = tk.Button(
            formFooter,
            text="Apply",
            image=images.checkIcon, # adds the check icon to the button
            compound=tk.LEFT,
            # on click, the profile preferences will be applied to the timezones/clocks in the main program
            command=lambda: profileTZSet(tM,tM2,tM3,tz,tz2,tz3,formEntryList,2,3,4,nestedCommand),
            width=125,
            height=40)
        # packs button to the grid
        formButton.grid(
            row=rownum,
            column=colnum,
            sticky="W,E,S,N",
            padx=(5),
            pady=(10, 10))
        return formButton

    # the formImportButtonWrapper() function creates the load profile button within the profile menu.
    def formImportButtonWrapper(rownum,colnum):
        formButton = tk.Button(
            formFooter,
            text="Load Profiles",
            image=images.uploadIcon,
            compound=tk.LEFT,
            # on click, the preferences/profile stored within the JSON and database will be loaded into the selected menu.
            command=lambda: readAndReplace(0,"testprefs"),
            width=125,
            height=40)
        # packs button to the grid
        formButton.grid(
            row=rownum,
            column=colnum,
            sticky="W,E,S,N",
            padx=(5),
            pady=(10, 10))
        return formButton

    # the formExportButtonWrapper() function creates the save profile button within the profile menu.
    def formExportButtonWrapper(rownum,colnum,profileNum):
        formButton = tk.Button(
            formFooter,
            text="Save Profiles",
            image=images.downloadIcon,
            compound=tk.LEFT,
            # on click, the user inputs for profile preferences will be saved into the JSON and database.
            command=lambda: profilePropertyPrinter(formEntry,formEntry2,formEntry3,formEntry4,formEntry5,profileNum),
            width=125,
            height=40)
        # packs button to the grid
        formButton.grid(
            row=rownum,
            column=colnum,
            sticky="W,E,S,N",
            padx=(5),
            pady=(10, 10))
        return formButton   

    # test StringVar() for Dropdown below
    testVar = tk.StringVar()
    # formDropdown creates the dropdown option list within the profile menu
    formDropdown = ttk.OptionMenu(
        formHeading,
        testVar,
        "Select an Option",
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
    # the setOptions() function sets the dropdown menu's option list
    def setOptions():
        formDropdown.set_menu(*dataList)
    setOptions = setOptions()

    # creating and packing every widget to the tkinter/gui grid
    formLabelWrapper(0,"Name:",formForm,1)
    formLabelWrapper(1,"Business:",formForm,1)
    formLabelWrapper(2,"Timezone 1:",formForm,1)
    formLabelWrapper(3,"Timezone 2:",formForm,1)
    formLabelWrapper(4,"Timezone 3:",formForm,1)
    formEntry = formEntryWrapper(0,formEntryVar)
    formEntry2 = formEntryWrapper(1,formEntryVar2)
    formEntry3 = formEntryWrapper(2,formEntryVar3)
    formEntry4 = formEntryWrapper(3,formEntryVar4)
    formEntry5 = formEntryWrapper(4,formEntryVar5)

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

# addProfileWrapper creates a tkinter button widget that allows the user to set the timezone values to default.
def addProfileWrapper(tM,tM2,tM3,tz,tz2,tz3):
    addProfileButton = tk.Button(
        menuFrame,
        text="Set Profile to Default",
        image=images.undoIcon,
        compound=tk.LEFT,
        command=lambda: profileTZSet(tM,tM2,tM3,tz,tz2,tz3,timezoneList2,0,1,2,None),
        width=200,
        height=40)
        # packs button to the grid
    addProfileButton.grid(
        row=0,
        column=1,
        sticky="W,E,S,N",
        padx=5,
        pady=(10,10))

# newWindow creates a tkinter button widget that opens the profile menu by running createNewWindow() on click
newWindow = tk.Button(
    menuFrame,
    # text="Create New Profile",
    text="Profile Menu",
    image=images.profileIcon,
    compound=tk.LEFT,
    command=lambda: createNewWindow(),
    width=125,
    height=40)
# packs button to the grid
newWindow.grid(
    row=0,
    column=2,
    sticky="S,N",
    padx=5,
    pady=(10,10))

# profileGreeting is a text field that greets the user, based on the name of the profile they are accessing.
profileGreeting = tk.Label(
    menuFrame,
    text=("Welcome, {}!".format(printEntry(formProfileVar))),
    font=("Arial", 12))
# packs label to the grid
profileGreeting.grid(
    row=0,
    column=3, 
    sticky="WESN", 
    pady=10)

# adds the "profileIcon" image to the newWindow button
newWindow.photoImage=images.profileIcon

# makeMapButton is a function that creates buttons to open up a flask environment with a google map and waypoint corresponding to coordinates that derive from the current user input within the timezone entry fields.
# this is done by running the gmplotTest.gMapPlot() function. (see gmplotTest.py)
def makeMapButton(rownum, entry):
    coordsList = getCoords(entry)
    locLat = coordsList[0]
    locLong = coordsList[1]
    # creation and properties of button widget
    mapButton = tk.Button(
        mapFrame,
        text="",
        image=images.mapIcon,
        compound=tk.LEFT,
        command=lambda: gmplotTest.gMapPlot(locLat,locLong),
        width=50,
        height=50)
    # packs button to the grid
    mapButton.grid(
        row=rownum,
        column=0,
        sticky="W,E,S,N",
        padx=(5),
        pady=(35))
    return mapButton

# timezoneMenus - entry fields that are used to input timezones for the displayed clocks, used as variables for clock functions below
timezoneMenu = makeTimezoneMenu(1, timezoneVar)
timezoneMenu2 = makeTimezoneMenu(2, timezoneVar2)
timezoneMenu3 = makeTimezoneMenu(3, timezoneVar3)

# run clock functions, creating labels and buttons
clock(makeGuiClockWrapper(makeTimezoneButton(1), 1, "tzVar1", timezoneMenu), "tzVar1")
clock(makeGuiClockWrapper(makeTimezoneButton(2), 2, "tzVar2", timezoneMenu2), "tzVar2")
clock(makeGuiClockWrapper(makeTimezoneButton(3), 3, "tzVar3", timezoneMenu3), "tzVar3")
makeMapButton(0,timezoneMenu)
makeMapButton(1,timezoneMenu2)
makeMapButton(2,timezoneMenu3)
addProfileWrapper(timezoneMenu, timezoneMenu2, timezoneMenu3, "tzVar1", "tzVar2", "tzVar3")

# used to sort weighting/spacing of rows and columns inside frames
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
