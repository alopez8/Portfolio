#Utils.py
#contains various utility functions for LightsGUI.py


from tkinter import *


import os

timeout_val = 4 #4 seconds before function is timeout

def GetBulbInfo(debug): #DONE #DOCSTRING #WORKS
    """_summary_
    Checks the './devices' directory for txt files containing device information. Loads the information into a dictionary for use with other functions.
    Only ID, name, model_description, and group are allowed.
    Lines that start with '#' are ignored.

    Arguments:
        debug -- Boolean: print information for debugging purposes.

    Returns:
        bulbs_dict -- dictionary: nested dictionary that contains all device name/model/group/id information. primary key is a meaningless number for looping over dictionary.
    """    
    
    if (debug): print(os.getcwd())
    try:
        if (debug): print(os.listdir('./devices'))
    except:
        print('Error: There is no "./devices" directory.')

    bulbs_dict = {}
    bulb_name = ''
    bulb_group = ''
    bulb_id = ''
    bulb_model = ''

    for root, dirs, files in os.walk("./devices"):
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(root, file).replace("\\", "/")
                if (debug): print('Opening file %s' % filepath)
                groupnamedefault = file[:file.find('.')]
                if (debug): print('Setting default bulb_group: %s' % groupnamedefault)
            
                #open the file
                try:
                    fopen = open(filepath, 'r')
                except:
                    print('Error: Could not open file: {}'.format(filepath))
            
                counter = 0
                #read file and save Bulb IDs
                for line in fopen:
                    if line.startswith('#'):
                        continue
                    elif line.lower().startswith('nickname'):
                        bulb_name = line[line.find(':')+1:].strip()
                    elif line.lower().startswith('group'):
                        bulb_group = line[line.find(':')+1:].strip()
                    elif line.lower().startswith('model:'): 
                        bulb_model = line[line.find(':')+1:].strip()
                    elif line.lower().startswith('id:'): #ID must come last. So add everything to a dictionary
                        bulb_id = line[line.find(':')+1:].strip()
                        
                          
                        #check if bulb has a group
                        if bulb_name == '': #use ID as default nickname
                            bulb_name = bulb_id
                        if bulb_group == '': #use filename as default group name
                            bulb_group = groupnamedefault 
                        if bulb_model == '':
                            bulb_model = 'Unknown' #use UNKNOWN if the bulb model is not available
                        
                        if (debug): print('bulb_name: |%s|' % bulb_name)   
                        if (debug): print('bulb_group: |%s|' % bulb_group)  
                        if (debug): print('bulb_model: |%s|' % bulb_model)  
                        if (debug): print('bulbID: |%s|' % bulb_id)    
                        
                        #check if this ID is already in the dictionary
                        if not any(bulb_id in d.values() for d in bulbs_dict.values()):
                            bulbs_dict[counter] = {}
                            if (debug):
                                print('ID not in dictionary')
                                print('ID %s' % bulb_id)
                                print(bulbs_dict)
                            #add 'name':'[name]' and 'ID': '[ID]', 'group': '[group] key-value pairs 
                            bulbs_dict[counter]['name'] = bulb_name
                            bulbs_dict[counter]['ID'] = bulb_id
                            bulbs_dict[counter]['group'] = bulb_group
                            bulbs_dict[counter]['model'] = bulb_model
                            counter += 1
                                            
                        #reset variables for next line in file
                        bulb_name = ''
                        bulb_group = ''
                        bulb_model = ''
                        bulb_id = ''
                        
                if (debug) and counter == 0: print('No bulb IDs found in file %s' % filepath)
                    
    
    return bulbs_dict  

def clearText(text): #DONE #DOCSTRING #WORKS
    """_summary_
    Removes all text from the text widget

    Arguments:
        text -- text widget
    """    """"""
    
    text.config(state=NORMAL)
    text.delete('1.0',END)
    text.config(state=DISABLED)
    
def findBulbstoChange(AddBulbs,GroupsToChange,BulbsFromFile): #DONE #DOCSTRING #WORKS
    """_summary_
    Simple function that checks checkboxes and returns a a list of IDs and a list of device names.

    Arguments:
        AddBulbs -- list of IntVar containing checkboxes results for which devices to change. Indices match BulbsFromFile entries.
        GroupsToChange -- dictionary: containing group name and IntVar determining whether to include those devices. 
        BulbsFromFile -- Dictionary containing all device information saved in the local text files.
        

    Returns:
        bulbstochange -- list of device ids to change
        bulbstochange_name -- list of device names to change. The indices match i.e. bulbstochange[i] goes with bulbstochange_name[i]
    """
    
    #loop over zipped GroupsToChange
    AddGroup = []
    for i in GroupsToChange:
        if GroupsToChange[i].get():
            AddGroup.append(i)
    
    bulbstochange = []
    bulbstochange_name = []
    for i in range(len(BulbsFromFile)):
        if AddBulbs[i].get() or BulbsFromFile[i]['group'] in AddGroup:
            bulbstochange.append(BulbsFromFile[i]['ID'])
            bulbstochange_name.append(BulbsFromFile[i]['name'])
            
    return bulbstochange,bulbstochange_name    
    
def BulbisAvailable(id,list): #DONE #DOCSTRING #WORKS
    """_summary_
    Check if device ID is found within BulbScanner.found_bulbs (i.e. ipaddress etc. are available)

    Arguments:
        id -- ID of device
        list -- list containing dictionary for each connected/available device

    Returns:
        Boolean indicating if the device ID is found within the scanner object.
    """
    
    #check if bulb ID is reachable through flux_led scanner
    if not any(id in bulb.values() for bulb in list):
        return False
    else:
        return True        
        
def get_display_size(): #DONE #DOCSTRING #WORKS    
    """_summary_
    returns the size of the user display

    Returns:
        height of user display measured in pixels
        width of user display measured in pixels
    """    
    root = Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', False)
    root.state('iconic')
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()
    return height, width


