#LightsGui.py
#GUI to control devices with the flux_led module (flux_led documentation: https://github.com/Danielhiversen/flux_led)
#use TKinter to develop GUI

#Author: Andrew Lopez
#Date: March 2023


from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import scrolledtext
from utils import * #import necessary functions from utils.py
from flux_led import BulbScanner, WifiLedBulb 
import os
from itertools import cycle #to use cycle function
import time


waittime = 0.3 #time in seconds to wait after changing a property. Some of my devices have a short delay (0.3 s) before refreshState() will detect a change.

commoncolors = [
    'Red: (255, 0, 0)',
    'Yellow: (255, 125, 0)',
    'Green: (0, 255, 0)',
    'Turquoise: (0, 255, 125)',
    'Blue: (0, 0, 255)',
    'Violet: (125, 0, 255)',
    'Pink: (255, 0, 125)',
    'White: (255, 255, 255)', 
]

red =  (255, 0, 0)
yellow = (255, 125, 0)
green = (0, 255, 0)
turquoise = (0, 255, 125)
blue = (0, 0, 255)
violet = (125, 0, 255)
pink = (255, 0, 125)
white = (255, 255, 255) 
colorwheel = [
        white,
        red,
        blue,
        yellow,
        pink,
        violet,
        green,
        turquoise,
]


def scanWindow(): #DONE #DOCSTRING #WORKS
    """_summary_
        Forgets all frames and places the Frame for the device scanner.
    """
    
    frame_scanWindow.grid(column = 0, row = 1,sticky=W)
    frame_changeWindow.grid_forget()
    
    clearText(txt_outputMessage)
    txt_outputMessage.config(state=NORMAL)
    txt_outputMessage.insert(END,'This Tab will scan for devices on the network and save the information to a file in the "./devices" directory. This file is necessary to use the Change functions.\n\nFor easier device identification, please check the "Change Device Colors" box. This WILL change the color/brightness of all available devices.\n')
    txt_outputMessage.config(state=DISABLED)

def changeWindow(): #DONE #DOCSTRING #WORKS
    """_summary_
        Forgets all frames and places the Frame for the device changer.
    """
    
    frame_changeWindow.grid(column = 0, row = 1,sticky=W)
    frame_scanWindow.grid_forget()
    
    clearText(txt_outputMessage)
    txt_outputMessage.config(state=NORMAL)
    txt_outputMessage.insert(END,'This Tab will load the list of devices from a file. Once loaded you can change the device Color/Brightness/State.\n\nIf there is no device file in the "./devices" directory please create one using the \'Device Scanner\' function.\n')
    txt_outputMessage.config(state=DISABLED)

def saveBulbInfo(ent_filename,ids,models,names,groups): ##DONE #DOCSTRING #WORKS
    """_summary_
    Saves the device information [scanner results (id, model) and user entries (name, group)] to a text file.
    File saved to ./devices directory. Default filename is 'DeviceInfo'. Default device name is [ID]. Default device group is 'None'.
    

    Arguments:
        ent_filename -- string: user entry that chooses file name of output text file. Default filename is 'DeviceInfo'. 
        ids -- list[string]: list of device ids found with the scanner.
        models -- list[string]: list of device model descriptions found with the scanner.
        names -- list[string]: list of device names input by user with entries. Default name is [ID].
        groups -- list[string]: list containing group of each device. Default group is 'None'.
    """
    
    txt_outputMessage.config(state=NORMAL)
    
    default_filename = 'DeviceInfo'
    if ent_filename.get() == '':
        filename = default_filename
    else:
        filename = ent_filename.get()
    
    homepath = os.getcwd().replace("\\","/")
    filepath = homepath+'/devices'+'/%s.txt' %filename

    try:
        f = open(filepath,'w')
    except:
        txt_outputMessage.insert(END,'\nInfo not saved. The directory "./devices" does not exist.\n')
        return
        
    f.write("#only nickname, group, model_description and id are used. nickname and group are not required. ID must come after nickname/group.\n\n")
    for i in range(len(ids)):
        id = ids[i]
        model = models[i]
        name = names[i].get()
        group = groups[i].get()
        
        if name == '':
            name = id
        if group == '':
            group = 'None'
        
        f.write("nickname: %s\n" % name)
        f.write("group: %s\n" % group)
        f.write("model: %s\n" % model)
        f.write("id: %s\n\n" % id)
        
    f.close()
    txt_outputMessage.insert(END,'Device information saved to \n"%s".\n' % filepath)
    txt_outputMessage.config(state=DISABLED)
    
def checkAvailability(scanner,BulbsFromFile): #DONE #DOCSTRING #WORKS
    """_summary_
    Re-scans the available devices and updates device selection table with results. 

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
    """
    
    ScanBulbs(scanner)
    for i in BulbsFromFile:
        available = ''
        if not BulbisAvailable(BulbsFromFile[i]['ID'],scanner.found_bulbs):
            available = 'N'
        else:
            available = 'Y'
        ttk.Label(frame_changeWindow, text = available).grid(column =5,row = 4+int(i),sticky=W) 

def ScanBulbs(scanner): #DONE #DOCSTRING #WORKS
    """_summary_
    Access scan function of flux_led BulbScanner class and update class with results (BulbScanner() object)

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
    Returns:
        Nothing
    """

    ##try to get bulb with ID
    scanner.scan(timeout=timeout_val) #scanner.found_bulbs now contains list of dictionaries about individual found bulbs. Order is randomized each time .scan() is run.

    return   

def clicked_LightScanner(scanner,ChangeColors): #DONE #DOCSTRING #WORKS
    """_summary_
    User has clicked Scan button. Print table of device info (ID label, model label, color-brightness label, name entry, group entry). Also create filename entry. Create Save button to allow saving this data to a local file for use with the other color-changing function.

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        ChangeColors -- Boolean flag indicating whether or not to change all available device colors/brightness for easier identification.
    """
    
    #recreate all widgets in frame_scanWindow EXCEPT btn_scan and checkbutton_ChangeColors ([0], and [1])
    widgetcount = 0
    for item in frame_scanWindow.winfo_children():
        if widgetcount > 1:
            item.destroy()
        widgetcount += 1
    
    clearText(txt_outputMessage) #clears entire text box
    txt_outputMessage.config(state=NORMAL)
    
    ScanBulbs(scanner)
    
    #define frame and labels for columns
    lbl_BulbID = Label(frame_scanWindow, text = 'Bulb ID')
    lbl_BulbID.grid(column=0,row = 2,sticky=W)
    lbl_BulbModel = Label(frame_scanWindow, text = 'Model Description')
    lbl_BulbModel.grid(column = 1,row = 2, padx=[10,0],sticky=W)
    lbl_BulbRGBB = Label(frame_scanWindow, text = 'RGB Color-Brightness')
    lbl_BulbRGBB.grid(column=2,row = 2,sticky=W)
    
    lbl_Bulbname = Label(frame_scanWindow, text = 'Bulb Name')
    lbl_Bulbname.grid(column=3,row = 2,sticky=W)
    
    lbl_Bulbgroup = Label(frame_scanWindow, text = 'Group Name')
    lbl_Bulbgroup.grid(column=4,row = 2,sticky=W)
    
    
    #create labels/entries for each bulb (name,ID,group,model,isavailable)
    ids = []
    names = []
    groups = []
    models = []
    
    counter = 0
    colorpool = cycle(colorwheel)
    brightness = 280
    for i in scanner.found_bulbs:
        id = i['id']
        bulb_info = scanner.getBulbInfoByID(id)
        try:
            bulb = WifiLedBulb(bulb_info["ipaddr"])
        except:
            txt_outputMessage.insert(END,'Device %s is not available.\n' % id)
            continue
        
        model = bulb.model_data.description
        
        #check if devices should be changed for easy identification
        if ChangeColors.get() == 1:
            #check if device can use RGB colors. if not: Do nothing
            if 'RGB' in bulb.color_modes:
                color = next(colorpool)
                if color == (255,255,255):
                    brightness = brightness - 25
                    if brightness < 0:
                        brightness = 255
                bulb.setRgb(*color,brightness = brightness)
            time.sleep(waittime)
            bulb.refreshState() #refreshes the WifiLedBulb state
            
        #convert brightness int to percentage
        brightnessval = str(round(bulb.brightness*100/255))+'%'
        
        #get the device RGB color and Brightness
        rgbval = ''
        if bulb.color_mode == 'RGB':
            rgbval = bulb.getRgb()
        elif bulb.color_mode == 'CCT':
            rgbval = 'CCT'
        else:
            rgbval = 'Unknown'
        RGBB = str(rgbval)+' - '+brightnessval
        
        #create id, model, and color labels for the device
        ttk.Label(frame_scanWindow, text = id).grid(column=0,row = 3+counter,sticky=W)
        ttk.Label(frame_scanWindow, text = bulb.model_data.description).grid(column=1,row = 3+counter, padx=[10,0],sticky=W)
        ttk.Label(frame_scanWindow, text= RGBB).grid(column =2,row = 3+counter,sticky=W )
        
        #create name, group entries for the device
        ent_name = Entry(frame_scanWindow) #name entry 
        ent_name.grid(column =3,row = 3+counter,sticky=W ) 
        ent_group = Entry(frame_scanWindow) #group entry
        ent_group.grid(column =4,row = 3+counter,sticky=W )
        
        #add id str, model str, and name/group entry widgets to lists. Allows easy passing to saveBulbInfo function.
        ids.append(id) 
        models.append(model)
        names.append(ent_name) ## works only if .grid is on separate line
        groups.append(ent_group) ## works only if .grid is on separate line
        counter += 1
    
    #create frame for save function button/label/entry widgets
    frame_saveInfo = Frame(frame_scanWindow)
    frame_saveInfo.grid(column = 0,columnspan = 4, row = 3+len(scanner.found_bulbs),sticky=W)
    
    #create and place save function label/button/entry widgets
    lbl_filename = Label(frame_saveInfo,text = 'Enter Filename:')
    lbl_filename.grid(column =0, row = 0,sticky=E)
    ent_filename = Entry(frame_saveInfo)
    ent_filename.grid(column = 1, row = 0)
    #create button to print data to file
    btn_saveInfo = Button(frame_saveInfo, text = 'Save Info', command = lambda: saveBulbInfo(ent_filename,ids,models,names,groups))
    btn_saveInfo.grid(column =2, row = 0)
    
    #print output message
    txt_outputMessage.insert(END, 'Found %s available devices. Scan again if more devices are connected.\nPlease enter optional names and groups for each device.\nTo use other functions, first save these devices with the "Save Info" button.\n' %len(scanner.found_bulbs))
    txt_outputMessage.config(state=DISABLED)

def clicked_TurnOn(scanner,AddBulbs,GroupsToChange,BulbsFromFile): #DONE #DOCSTRING #WORKS
    """_summary_
    Get devices to change and turn them all on.

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
    """
    
    txt_outputMessage.config(state=NORMAL)
    counter = 0
    
    bulbstochange, bulbstochange_name = findBulbstoChange(AddBulbs,GroupsToChange,BulbsFromFile) 
    
    if len(bulbstochange) == 0:
        txt_outputMessage.insert(END,'No devices selected.')
        return
    else:
        txt_outputMessage.insert(END,'Turning on %s devices.\n' % str(len(bulbstochange)))
        
    for i in range(len(bulbstochange)):
        #check if bulb is available
        id = bulbstochange[i]
        name = bulbstochange_name[i]
        if not BulbisAvailable(id,scanner.found_bulbs):
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
              
        #Get info for a specific bulb
        bulb_info = scanner.getBulbInfoByID(id) #class with bulb info
        
        #use IP address to get bulb as a wifiLEDBulb object
        try:
            bulb = WifiLedBulb(bulb_info["ipaddr"])
        except:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
        
        if bulb.is_on:
            counter += 1
            continue
        bulb.turnOn()  
        time.sleep(waittime)
        bulb.refreshState()
        if bulb.is_on:
            counter += 1
        else:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) failed to turn on.\n' % (name,id))
            
    txt_outputMessage.insert(END,'Successfully turned on %s devices.\n' % str(counter))
    txt_outputMessage.config(state=DISABLED)

def clicked_TurnOff(scanner,AddBulbs,GroupsToChange,BulbsFromFile): #DONE #DOCSTRING #WORKS
    """_summary_
    Get devices to change and turn them all off.

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
    """
    
    txt_outputMessage.config(state=NORMAL)
    counter = 0
    
    bulbstochange, bulbstochange_name = findBulbstoChange(AddBulbs,GroupsToChange,BulbsFromFile) 
    
    if len(bulbstochange) == 0:
        txt_outputMessage.insert(END,'No devices selected.')
        return
    else:
        txt_outputMessage.insert(END,'Turning off %s devices.\n' % str(len(bulbstochange)))
        
    for i in range(len(bulbstochange)):
        #check if bulb is available
        id = bulbstochange[i]
        name = bulbstochange_name[i]
        if not BulbisAvailable(id,scanner.found_bulbs):
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
              
        #Get info for a specific bulb
        bulb_info = scanner.getBulbInfoByID(id) #class with bulb info
        
        #use IP address to get bulb as a wifiLEDBulb object
        try:
            bulb = WifiLedBulb(bulb_info["ipaddr"])
        except:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
        
        if not bulb.is_on:
            counter += 1
            continue
        bulb.turnOff()  
        time.sleep(waittime)
        bulb.refreshState()
        if not bulb.is_on:
            counter += 1
        else:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) failed to turn off.\n' % (name,id))
        
    txt_outputMessage.insert(END,'Successfully turned off %s devices.\n' % str(counter))
    txt_outputMessage.config(state=DISABLED)  
  
def clicked_WarmWhite(scanner,AddBulbs,GroupsToChange,BulbsFromFile,Brightness): #DONE #DOCSTRING #WORKS
    """_summary_
    Change selected devices to the Warm White CCT temperature (2700)

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
        Brightness --Entry: Contains optional brightness percentage value
    """
    
    txt_outputMessage.config(state=NORMAL)
    temperature = 2700  #cool = 6500, warm = 2700, middleground =4600
    successes = Change_CCT(scanner,AddBulbs,GroupsToChange,BulbsFromFile,Brightness,temperature)
    txt_outputMessage.insert(END,'Successfully changed %s devices to Warm White.\n' % successes)
    txt_outputMessage.config(state=DISABLED)

def clicked_CoolWhite(scanner,AddBulbs,GroupsToChange,BulbsFromFile,Brightness): #DONE #DOCSTRING #WORKS
    """_summary_
    Change selected devices to the Cool white CCT temperature (6500)

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
        Brightness --Entry: Contains optional brightness percentage value
    """    
    
    txt_outputMessage.config(state=NORMAL)
    temperature = 6500 #cool = 6500, warm = 6500
    successes = Change_CCT(scanner,AddBulbs,GroupsToChange,BulbsFromFile,Brightness,temperature)
    txt_outputMessage.insert(END,'Successfully changed %s devices to Cool White.\n' % successes)
    txt_outputMessage.config(state=DISABLED)

def Change_CCT(scanner,AddBulbs,GroupsToChange,BulbsFromFile,Brightness,temp): #DONE #DOCSTRING #WORKS
    """_summary_
    Change devices to a specific hard-coded CCT temperature (warm white or cool white).

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
        Brightness --Entry: Contains optional brightness percentage value
        temp -- int: CCT temperature

    Raises:
        Exception: Brightness value is not an integer between 0-100

    Returns:
        number of successful device changes.
    """    
    
    txt_outputMessage.config(state=NORMAL)
    
    bulbstochange, bulbstochange_name = findBulbstoChange(AddBulbs,GroupsToChange,BulbsFromFile) 
     
    if len(bulbstochange) == 0:
        txt_outputMessage.insert(END,'No devices selected.\n')
        return
    
    
    brightness_value_true = 0
    brightness_bad = False
    brightness_ignore = True
    if Brightness.get() != '':
        brightness_ignore = False
    
    if not brightness_ignore:
        try:
            brightness_value = int(Brightness.get())
            if brightness_value < 0 or brightness_value > 100:
                raise Exception("")
        except:
            brightness_bad = True
        
    if brightness_bad: 
        if brightness_bad: brightness_value = 'Invalid'
        txt_outputMessage.insert(END,'Invalid Brightness value: %s' % (brightness_value))
    else:
        if brightness_ignore:
            brightness_value = 'None'
        else:
            brightness_value_true = round(brightness_value*255./100.)

    if temp == 2700:
        txt_outputMessage.insert(END,'Changing %s devices to Warm White (Brightness: %s%%).\n' %(len(bulbstochange),brightness_value))
    elif temp == 6500:
        txt_outputMessage.insert(END,'Changing %s devices to Cool White (Brightness: %s%%).\n' %(len(bulbstochange),brightness_value))
    else:
        txt_outputMessage.insert(END,'Changing %s devices to temperature %s (Brightness: %s%%).\n' % (len(bulbstochange),temp,brightness_value))

    counter = 0
    for i in range(len(bulbstochange)):
        #check if bulb is available
        id = bulbstochange[i]
        name = bulbstochange_name[i]
        if not BulbisAvailable(id,scanner.found_bulbs):
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
        
        #Get info for a specific bulb
        bulb_info = scanner.getBulbInfoByID(id) #class with bulb info
                
        #use IP address to get bulb as a wifiLEDBulb object
        try:
            bulb = WifiLedBulb(bulb_info["ipaddr"])
        except:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
        if 'CCT' not in bulb.color_modes:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) has no \'CCT\' mode.\n' % (name,id))
            continue
        
        if brightness_ignore:
            brightness_value_true = bulb.brightness
        #change bulb temperature
        bulb.setWhiteTemperature(temperature = temp, brightness = int(brightness_value_true))

        #check if device has changed
        time.sleep(waittime)
        bulb.refreshState()
        if bulb.color_mode == 'CCT' and bulb.getWhiteTemperature()[0] == temp:
            counter += 1
        else:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) failed to change.\n' % (name,id))
    
    return counter

def clicked_ChangeBrightness(scanner,AddBulbs,GroupsToChange,BulbsFromFile,Brightness): #DONE #DOCSTRING #WORKS
    """_summary_
    Check entry widget 'brightness' is valid and start function to change bulb brightness of selected devices.
        
    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
        Brightness --Entry: Contains optional brightness percentage value

    Raises:
        Exception: Brightness value is not an integer between 0-100    
    """    
    
    txt_outputMessage.config(state=NORMAL)
    counter = 0
    
    
    brightness_bad = False
    try:
        brightness_value = int(Brightness.get())
        if brightness_value < 0 or brightness_value > 100:
            raise Exception("")
    except:
        brightness_bad = True
        
    if brightness_bad: 
        if brightness_bad: brightness_value = Brightness.get()
        txt_outputMessage.insert(END,'Invalid Brightness value.\n')
        return
    
    counter = Change_Brightness(scanner,AddBulbs,GroupsToChange,BulbsFromFile,brightness_value) #pass brightness_value as a percentage
    
    txt_outputMessage.insert(END,'Successfully changed brightness of %s devices.\n' % str(counter))
    txt_outputMessage.config(state=DISABLED)
 
def Change_Brightness(scanner,AddBulbs,GroupsToChange,BulbsFromFile,brightness_value): #DONE #DOCSTRING #WORKS
    """_summary_
    Change brightness of devices in list to the brightness value specified.

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
        brightness_value -- int: change devices to this brightness_value. written as a percentage.

    Returns:
        number of successfully changed devices.
    """    
    
    bulbstochange, bulbstochange_name = findBulbstoChange(AddBulbs,GroupsToChange,BulbsFromFile) 
    
    if len(bulbstochange) == 0:
        txt_outputMessage.insert(END,'No devices selected.\n')
        return
    
    txt_outputMessage.insert(END,'Changing brightness of %s devices to %s%%\n' % (str(len(bulbstochange)),brightness_value))
    brightness_value = round(brightness_value*255./100.)
    
    counter = 0
    for i in range(len(bulbstochange)):
        #check if bulb is available
        id = bulbstochange[i]
        name = bulbstochange_name[i]
        if not BulbisAvailable(id,scanner.found_bulbs):
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
        
        #Get info for a specific bulb
        bulb_info = scanner.getBulbInfoByID(id) #class with bulb info
                
        #use IP address to get bulb as a wifiLEDBulb object
        try:
            bulb = WifiLedBulb(bulb_info["ipaddr"])
        except:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
               
        if bulb.color_mode == 'RGB':
            bulb.setRgb(*bulb.getRgb(), brightness=int(brightness_value))   
        elif bulb.color_mode == 'CCT':
            bulb.setWhiteTemperature(temperature = bulb.getWhiteTemperature()[0], brightness = int(brightness_value))
        else:
            continue ##do nothing if color_mode is not RGB or CCT.
            
        #check if bulb has changed brightness to desired value
        time.sleep(waittime)
        bulb.refreshState()
        if bulb.brightness >= brightness_value-1 and bulb.brightness <= brightness_value+1:
            counter += 1
        else:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) failed to change brightness.\n' % (name,id))
        
    return counter

def clicked_ChangeBulbColors(scanner,AddBulbs,GroupsToChange,BulbsFromFile,R,G,B,Brightness): #DONE #DOCSTRING #WORKS
    """_summary_
    Check entry widgets 'R','G','B' and 'Brightness' are valid and start function to change bulb color of selected devices.

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
        R -- Entry widget: contains R value
        G -- Entry widget: contains G value
        B -- Entry widget: contains B value
        Brightness -- Entry widget: contains brightness value

    Raises:
        Exception: Invalid 'R' entry value. Not between 0-100.
        Exception: Invalid 'G' entry value. Not between 0-100.
        Exception: Invalid 'B' entry value. Not between 0-100.
        Exception: Invalid 'Brightness' entry value. Not between 0-100.
    """    
    
    txt_outputMessage.config(state=NORMAL)
    counter = 0
    
    r_bad = False
    g_bad = False
    b_bad = False
    brightness_bad = False
    brightness_ignore = True
    if Brightness.get() != '':
        brightness_ignore = False
    else:
        brightness_value = 'None'
        
    try:
        r_value = int(R.get())
        if r_value < 0 or r_value > 255:
            raise Exception("invalid_r")
    except:
        r_bad = True

    try:
        g_value = int(G.get())
        if g_value < 0 or g_value > 255:
            raise Exception("invalid_g")
    except:
        g_bad = True
        
    try:
        b_value = int(B.get())
        if b_value < 0 or b_value > 255:
            raise Exception("invalid_b")
    except: 
        b_bad = True
    
    if not brightness_ignore:
        try:
            brightness_value = int(Brightness.get())
            if brightness_value < 0 or brightness_value > 100:
                raise Exception("invalid_brightness")
        except:
            brightness_bad = True
        
    if r_bad or g_bad or b_bad or brightness_bad: 
        if r_bad: r_value = 'Invalid'
        if g_bad: g_value = 'Invalid'
        if b_bad: b_value = 'Invalid'
        if brightness_bad: brightness_value = 'Invalid'
        txt_outputMessage.insert(END,'Invalid RGB-Brightness value: (%s, %s, %s) %s%%\n' % (r_value,g_value,b_value,brightness_value))
        return

    counter = Change_Color(scanner,AddBulbs,GroupsToChange,BulbsFromFile,r_value,g_value,b_value,brightness_value,brightness_ignore)
        
    txt_outputMessage.insert(END,'Successfully changed color of %s devices.\n' % str(counter))
    txt_outputMessage.config(state=DISABLED)

def Change_Color(scanner,AddBulbs,GroupsToChange,BulbsFromFile,r_value,g_value,b_value,brightness_value,brightness_ignore): #DONE #DOCSTRING #WORKS
    """_summary_
    Change color of devices from given list to given color/brightness. For brightness to be set at 100%: at least one value RGB must equal 255, or brightness_value must be 100

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
        r_value -- int: value of RGB Red 0-255
        g_value -- int: value of RGB Green 0-255
        b_value -- int: value of RGB Blue 0-255
        brightness_value -- int/string: user given brightness value. if not brightness_ignore: int (as a percentage 0-100). if brightness_ignore: string ('None') 
        brightness_ignore -- Boolean: Whether to change the brightness or not
    """    
    
    bulbstochange, bulbstochange_name = findBulbstoChange(AddBulbs,GroupsToChange,BulbsFromFile) 
 
    if len(bulbstochange) == 0:
        txt_outputMessage.insert(END,'No devices selected.\n')
        return
    
    txt_outputMessage.insert(END,'Changing color of %s devices to RGB-Brightness: (%s,%s,%s) - %s%%\n' % (str(len(bulbstochange)),r_value,g_value,b_value,brightness_value))
    if not brightness_ignore:
        brightness_value = round(brightness_value*255./100.)
    
    ###change below to it's own function
    counter = 0
    for i in range(len(bulbstochange)):
        #check if bulb is available
        id = bulbstochange[i]
        name = bulbstochange_name[i]
        if not BulbisAvailable(id,scanner.found_bulbs):
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
        
        #Get info for a specific bulb
        bulb_info = scanner.getBulbInfoByID(id) #class with bulb info
                
        #use IP address to get device as a WifiLedBulb object
        try:
            bulb = WifiLedBulb(bulb_info["ipaddr"])
        except:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) is not available.\n' % (name,id))
            continue
        
        #check if color of device can be changed
        if 'RGB' not in bulb.color_modes:
            txt_outputMessage.insert(END,'Device "%s" (ID: %s) has no RGB color mode. Cannot change color.\n' % (name,id)) ##cannot test
            continue
          
        #check if brightness of device should/can be changed
        if brightness_ignore: #if a brightness has not been input
            bulb.setRgb(r_value, g_value, b_value) 
        else:
           bulb.setRgb(r_value, g_value, b_value, brightness=int(brightness_value))  
        counter += 1   #cannot explicitly check if color has changed. rgb is scaled down by brightness (ratio between RGB stays the same). For 100% brightness at least one number RGB must be 255.
    return counter  

def clicked_LoadBulbInfo(scanner): #DONE #DOCSTRING #WORKS
    """_summary_
    Load the device info from the device information txt file then allow the user to select which devices to change and which function to perform.

    Arguments:
        scanner -- object with the flux_led BulbScanner() Class.
    """    
    
    clearText(txt_outputMessage) #clears entire text box
    txt_outputMessage.config(state=NORMAL)
    
    ##recreate all widgets in frame_scanWindow EXCEPT btn_scan and checkbutton_ChangeColors ([0], and [1])
    widgetcount = 0
    for item in frame_changeWindow.winfo_children():
        if widgetcount > 3:
            item.destroy()
        widgetcount += 1
    
    
    BulbsFromFile = {}
    BulbsFromFile = GetBulbInfo(False)
    num_bulbs = len(BulbsFromFile)
    lbl_dictloadmessage['text'] = '%s devices have been loaded.' % num_bulbs 

    if num_bulbs == 0:
        txt_outputMessage.insert(END,'No devices have been loaded. Please make sure a device information text file is in the \'./devices\' directory.\nIf one is not, please use the \'Device Scanner\' tab.')
    

    ScanBulbs(scanner)

    #list all bulbs found in the dictionary
    #define frame and labels for columns
    lbl_dictAddBulb = Label(frame_changeWindow, text = 'Change?')
    lbl_dictAddBulb.grid(column=0,row = 3,sticky=E)
    lbl_dictBulbname = Label(frame_changeWindow, text = 'Device Name')
    lbl_dictBulbname.grid(column=1,row = 3,sticky=W)
    lbl_dictBulbID = Label(frame_changeWindow, text = 'Device ID')
    lbl_dictBulbID.grid(column=2,row = 3,sticky=W)
    lbl_dictBulbgroup = Label(frame_changeWindow, text = 'Group')
    lbl_dictBulbgroup.grid(column=3,row = 3,sticky=W)
    lbl_dictBulbmodel = Label(frame_changeWindow, text = 'Model')
    lbl_dictBulbmodel.grid(column=4,row = 3,sticky=W)
    lbl_dictBulbAvailable = Label(frame_changeWindow, text = 'Available')
    lbl_dictBulbAvailable.grid(column=5,row = 3,sticky=W)
    
    #create checkbutton/labels for each bulb (name,ID,group,available)
    AddBulbs = []
    GroupCheck = []
    groupslist = []
    for i in BulbsFromFile:
        if BulbsFromFile[i]['group'] not in groupslist:
            groupslist.append(BulbsFromFile[i]['group'])
        available = ''
        AddBulbs.append(IntVar(value = 0))
        ttk.Checkbutton(frame_changeWindow,variable = AddBulbs[-1]).grid(column=0,row = 4+int(i),sticky=E)
        ttk.Label(frame_changeWindow, text= BulbsFromFile[i]['name']).grid(column =1,row = 4+int(i),sticky=W )
        ttk.Label(frame_changeWindow, text= BulbsFromFile[i]['ID']).grid(column =2,row = 4+int(i),sticky=W )
        ttk.Label(frame_changeWindow, text= BulbsFromFile[i]['group']).grid(column =3,row = 4+int(i),sticky=W )
        ttk.Label(frame_changeWindow, text= BulbsFromFile[i]['model']).grid(column =4,row = 4+int(i),sticky=W )
        if not BulbisAvailable(BulbsFromFile[i]['ID'],scanner.found_bulbs):
            available = 'N'
        else:
            available = 'Y'
        ttk.Label(frame_changeWindow, text = available).grid(column =5,row = 4+int(i),sticky=W)
 
    #Add menubutton to control lights by group
    lbl_controlGroup = Label(frame_changeWindow,text = 'Control By Group:')
    lbl_controlGroup.grid(column = 0,columnspan = 1, row = 5+len(BulbsFromFile))
    
    mbtn_controlGroup = Menubutton(frame_changeWindow, text = 'Groups', relief = RAISED) 
    menu_group = Menu(mbtn_controlGroup, tearoff = 0)
    
    for i in groupslist:
        GroupCheck.append(IntVar(value = 0))
        menu_group.add_checkbutton(label = i,variable = GroupCheck[-1]) 

    mbtn_controlGroup['menu'] = menu_group
    mbtn_controlGroup.grid(column = 1,row = 5+len(BulbsFromFile),sticky='NEWS')
    
    GroupsToChange = dict(zip(groupslist,GroupCheck))
    
    #create button to recheck availability of bulbs
    btn_checkAvailability = Button(frame_changeWindow, text = 'Recheck Availability', command = lambda: checkAvailability(scanner,BulbsFromFile))  #########################
    btn_checkAvailability.grid(column =4, columnspan = 2, row = 1,sticky=E) #originally column = 5
        
    #create the entry and label widgets for the RGB-Brightness values  
    frame_rgbb = Frame(frame_changeWindow)
    frame_rgbb.grid(column = 0, columnspan = 7, row = 6+len(BulbsFromFile),sticky=W)
    
    #create and set up R frame, label, and entry widgets
    frame_r = Frame(frame_rgbb)
    frame_r.grid(column = 0, row = 0)
    lbl_r = Label(frame_r,text = 'R (0-255):')
    lbl_r.grid(column = 0,row = 0)
    entry_r = Entry(frame_r)
    entry_r.grid(column = 1,row = 0)
    
    #create and set up G frame, label, and entry widgets
    frame_g = Frame(frame_rgbb)
    frame_g.grid(column = 1, row = 0)
    lbl_g = Label(frame_g,text = 'G (0-255):')
    lbl_g.grid(column = 0,row = 0,padx = (10,0),sticky=E)
    entry_g = Entry(frame_g)
    entry_g.grid(column = 1,row = 0)
    
    #create and set up B frame, label, and entry widgets
    frame_b = Frame(frame_rgbb)
    frame_b.grid(column = 2, row = 0)
    lbl_b = Label(frame_b,text = 'B (0-255):')
    lbl_b.grid(column = 0,row = 0,padx = (10,0), sticky=E)
    entry_b = Entry(frame_b)
    entry_b.grid(column = 1,row = 0)
    
    #create and set up Brightness frame, label, and entry widgets
    frame_bright = Frame(frame_rgbb)
    frame_bright.grid(column = 0, row = 1)
    lbl_brightness = Label(frame_bright,text = 'Brightness (0-100) %:')
    lbl_brightness.grid(column = 0,padx = (10,0),row = 0, sticky=W)
    entry_brightness = Entry(frame_bright)
    entry_brightness.grid(column = 1,row = 0)
    
    
    #create a text widget to hold the RGB values for common colors
    lbl_colors = Label(frame_changeWindow,text = 'RGB of Common Colors')
    lbl_colors.grid(column = 6, row = 3)
    txt_colors = Text(frame_changeWindow,height = len(commoncolors), width = 20)
    txt_colors.grid(column = 6, row = 4, rowspan = len(BulbsFromFile),sticky=N)
    txt_colors.insert(END, '\n'.join(commoncolors))
    txt_colors.config(state=DISABLED)
    
    #create a frame to hold the buttons that change bulb settings
    frame_bulbchangebuttons = Frame(frame_changeWindow)
    frame_bulbchangebuttons.grid(column = 0, columnspan = 6, row = 8+len(BulbsFromFile))
    
    #create buttons that change bulb settings and place them in the special frame
    lbl_functions = Label(frame_bulbchangebuttons,text = 'Functions:')
    lbl_functions.grid(column = 0, padx=(0,10), row = 0,rowspan = 2)
    
    lbl_brightness_optional = Label(frame_bulbchangebuttons,text = '(Brightness optional)')
    lbl_brightness_optional.grid(column = 4, padx=(0,10), row = 0)
    #button changes RGB-Brightness value
    btn_change_colors = Button(frame_bulbchangebuttons,text = 'Change Colors', command = lambda: clicked_ChangeBulbColors(scanner,AddBulbs,GroupsToChange,BulbsFromFile,entry_r,entry_g,entry_b,entry_brightness))
    btn_change_colors.grid(column = 1,row = 0,sticky='news')
    
    #button turns bulbs to Warm-White 
    btn_WarmWhite = Button(frame_bulbchangebuttons,text = 'Set Warm White', command = lambda: clicked_WarmWhite(scanner,AddBulbs,GroupsToChange,BulbsFromFile,entry_brightness))
    btn_WarmWhite.grid(column = 2,row = 0,sticky='news')
    #button turns bulbs to Cold-White
    btn_CoolWhite = Button(frame_bulbchangebuttons,text = 'Set Cool White', command = lambda: clicked_CoolWhite(scanner,AddBulbs,GroupsToChange,BulbsFromFile,entry_brightness))
    btn_CoolWhite.grid(column = 3,row = 0,sticky='news')
    
    #button turns bulbs off
    btn_turnoff = Button(frame_bulbchangebuttons,text = 'Turn Devices Off', command = lambda: clicked_TurnOff(scanner,AddBulbs,GroupsToChange,BulbsFromFile))
    btn_turnoff.grid(column = 1,row = 1,sticky='news')
    #button turns bulbs on
    btn_turnon = Button(frame_bulbchangebuttons,text = 'Turn Devices On', command = lambda: clicked_TurnOn(scanner,AddBulbs,GroupsToChange,BulbsFromFile))
    btn_turnon.grid(column = 2,row = 1,sticky='news')
    #button changes the bulb brightness ONLY
    btn_change_brightness = Button(frame_bulbchangebuttons,text = 'Change Brightness', command = lambda: clicked_ChangeBrightness(scanner,AddBulbs,GroupsToChange,BulbsFromFile,entry_brightness))
    btn_change_brightness.grid(column = 3,row = 1,sticky='news')

    txt_outputMessage.config(state=DISABLED)
    
       
######################### MAIN program ##########################


root=Tk() #This automatically creates a graphical window with the title bar, minimize, maximize and close buttons.
# root window title and dimension
root.title("LightsGUI")

#get user resolution and set geometry
height, width = get_display_size()
if width >= 1152:
    font = 'Arial 14'
    winWidth = 1152
elif width < 1152 and width >= 960:
    font = 'Arial 13'
    winWidth = 960
else:
    font = 'Arial 10'
    winWidth = width
winHeight = height
geo = str(winWidth)+'x'+str(winHeight)+'+0+0' #start window in top left corner of user screen
root.geometry(geo)

#Change default font type and size
root.option_add( "*font", font)#"Arial 14" ) #I think 14 is good size

#define scanner object
scanner = BulbScanner()  #Class that contains functions to easily select/modify device settings.


############# Root Frame Widgets ##########################
#Define buttons 
frame_window = Frame(root)
frame_window.grid(column = 0, row = 0,columnspan=10,rowspan = 30)
frame_menu = Frame(frame_window)
frame_menu.grid(column = 0, columnspan=10,row = 0,sticky=W)

#Change Bulbs button 
btn_changeBulbs = Button(frame_menu, text = "Change Devices" ,fg = "black", command = changeWindow)
#Scanner button 
btn_Scanner = Button(frame_menu, text = "Device Scanner" ,fg = "black",command = scanWindow)

#set button positions
btn_changeBulbs.grid(column = 0, row=0)
btn_Scanner.grid(column = 1, row=0)

#Define other window frames
frame_changeWindow = Frame(frame_window)
frame_scanWindow = Frame(frame_window)
frame_outputMessage = Frame(frame_window)
frame_outputMessage.grid(column = 0, row = 2)


########### changeWindow Frame  Widgets ############
btn_LoadBulbs = Button(frame_changeWindow,text='Load Devices from File',command = lambda: clicked_LoadBulbInfo(scanner))
btn_LoadBulbs.grid(column = 0,columnspan = 2, row = 1,sticky=W)
lbl_dictloadmessage = Label(frame_changeWindow, text = '0 bulbs have been loaded.')
lbl_dictloadmessage.grid(column=2,columnspan = 3,row = 1,sticky=W)


###### output message box #########
txt_outputMessage = scrolledtext.ScrolledText(frame_outputMessage, height = 10, width = 70,wrap=WORD)
txt_outputMessage.grid(column = 0, row = 0, rowspan = 10,sticky=N)
txt_outputMessage.insert(END, 'Welcome. Please select a tab to begin.\n\nDeveloped by Andrew Lopez.\nGithub: https://github.com/alopez8\nItch.io: https://jydin.itch.io/')
txt_outputMessage.config(state=DISABLED)
btn_clearoutputMessage = Button(frame_outputMessage, text = 'Clear Messages',command = lambda: clearText(txt_outputMessage))
btn_clearoutputMessage.grid(column = 1, row = 0)

    
########### scanWindow Frame Widgets #############
ChangeColors = IntVar()
btn_Scan = Button(frame_scanWindow, text = "Scan",fg = "black",command = lambda: clicked_LightScanner(scanner,ChangeColors)) 
btn_Scan.grid(column = 0, row = 1,sticky=W)
btn_ChangeColors = Checkbutton(frame_scanWindow,text='Change Device Colors',fg = 'black', variable = ChangeColors)
btn_ChangeColors.grid(column = 1, row = 1,sticky=W)


# Execute Tkinter
root.mainloop() # This method says to take all the widgets and objects we created, render them on our screen, and respond to any interactions. The program stays in the loop until we close the window.



