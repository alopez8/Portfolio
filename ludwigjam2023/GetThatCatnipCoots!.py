#GetThatCatnipCoots!
"""
Designed for the Ludwig Jam 2023

author/designer/programmer: Andrew Lopez
email: jydin.lopez@gmail.com
date started: Feb. 16, 2023
date finished: Feb. 25, 2023

Abstract: This is a short text based adventure game where you help Coots reach the catnip on the counter.

Credits:
Sound Effects: 'And The Winner Is' (CC0) and 'Total Fail' (CC0) by congusbongus
Font: 'AC437 IBM VGA 8x16' by VileR (Website: https://int10h.org/oldschool-pc-fonts/) under CC BY-SA 4.0
Inspired by the browser game "Don't Shit Your Pants" by Teddy Lee and Kenny Lee for Cellar Door Games.

ToDo:

Notes:
All commands and objects are in the respective lists.
timer is working properly
get response/check command function are working properly
all endings are coded into the game
Response/location text is being split into multiple lines in the display by using '+' as a separator
"""

#define available commands
commands = ['start','quit','endings','credits','poop','look','climb','extend','retract','jump','open','get','push','help','listcommands','listobjects'] #All 16 commands

#text for help command
text_help = 'Inputs can be one or two words:  one COMMAND and an optional OBJECT.+Inputs are not case sensitive.+If you are stuck try the LOOK command by itself or with an OBJECT.+For the complete list of COMMANDs type LISTCOMMANDS.+For the complete list of OBJECTs type LISTOBJECTS.'

#text for listcommands command
text_listcommands = "The possible commands are:+{}+{}".format(', '.join(commands[:8]).upper(), ', '.join(commands[8:]).upper())


#define objects available in game
objects = ['cabinet','catnip', 'claws','counter','drapes','nami'] #All 6 objects

#text for list objects command
text_listobjects = 'The possible objects are:+{}'.format(', '.join(objects).upper())

#Text for ending page
endings_achieved = ['','','','','','','']
ending_timer = 0 #ending 1
ending_drapes = 1 #ending 2
ending_nami = 2 #ending 3
ending_poop = 3 #ending 4
ending_lostcatnip = 4 #ending 5
ending_caught = 5 #ending 6
ending_escaped = 6 #ending 7
text_ending = [ #DONE
                'ENDING 1: Out of Time ', 
                'ENDING 2: Prince of Purrsia Wannabe ',
                'ENDING 3: Like Father, Like Son ',
                'ENDING 4: You Have A Litter Box You Know ',
                'ENDING 5: Plummeting Catnip ',
                'ENDING 6: Caught Red-Pawed ',
                'ENDING 7: Escaped! '
               ]

outcome_endings = [ #DONE
                    'As the footsteps grow closer, you see Ludwig enter the kitchen.+Unfortunately, while he is around you will not be able to get the catnip.+You slink off to your scratching post to work off your frustration.++ENDING 1: Out of Time',
                    'Fighting against your instincts, you retract your claws.+Without them you begin to slide down the drapes and crash into the floor.+As you lick your bruised paw you realize you will not be getting any catnip today.++ENDING 2: Prince of Purrsia Wannabe',
                    'You fall victim to the charm of the Nami figurine.+Ludwig enters the kitchen to see you holding it gently.+You will no longer be able to get any catnip but for some reason you are not very disappointed.++ENDING 3: Like Father, Like Son',
                    'You have pooped and made a mess everywhere.+After finishing your business, you find you do not remember why you came to the kitchen.++ENDING 4: You Have A Litter Box You Know',
                    'You surrender to a dark impulse and push the cantip off of the counter.+Ludwig sees the catnip mess you have made and sweeps all of the catnip into the trash.+You realise that there is no longer catnip in the house.+Your despair is immense and eternal.++ENDING 5: Plummeting Catnip ',
                    'You grab the catnip but are quickly caught when Ludwig enters the room.+If only there was some way to distract him...++ENDING 6: Caught Red-Pawed',
                    'With catnip in your mouth, you dash out of the room while Ludwig+tries in vain to collect all of the pieces of the broken Nami figurine.++ENDING 7: Escaped!'
                  ]

#text for credits page
text_credits = ['Designer/Programmer: Andrew Lopez',"Sound Effects: 'And The Winner Is' and 'Total Fail' by congusbongus","Font: 'AC437 IBM VGA 8x16' by VileR (Website: https://int10h.org/oldschool-pc-fonts/)","Inspired by: 'Don't Sh*t Your Pants' by Teddy Lee and Kenny Lee for Cellar Door Games"]#DONE

#define dictionaries for each command response
text_quit = 'Thank you for playing!'
text_extend_claws = {#DONE
                        'True': 'You EXTEND your sharp CLAWS.+Nature\'s perfect CLIMBing tools.',
                        'False': 'Your CLAWS are already EXTENDed. Did you mean to RETRACT them?' 
                    }
text_retract_claws = { #DONE
                        'True': 'Your CLAWS are already RETRACTed. Did you mean to EXTEND them?',
                        'False': 'You RETRACT your deadly CLAWS.',
                    }


#define locations
locations = ['menu','floor','drapes','counter','endings','credits'] #DONE

#Define location message that constantly displays 
text_location_dict = { #DONE
                  'menu': 'This is a text based adventure game. None of the inputs are case sensitive.+Type HELP if you get stuck+Type START to begin the game. Type QUIT to return to this screen.+Type EXIT to end the program+Type CREDITS to view the credits+Type ENDINGS to view the endings you have achieved',
                  'floor': 'You are on the kitchen floor.+You can smell CATNIP on top of the COUNTER.+You hear footsteps coming down the hall.',
                  'drapes': "You are hanging on the DRAPES.+The COUNTER is just within your reach.", 
                  'counter': "You are on top of the COUNTER.+The CATNIP smell is very strong.+It seems to be coming from the CABINET...",
                  'endings': '++Available Endings:',
                  'credits': '++Credits:',
                  }

#outcome for each location
outcome_floor = { #DONE
                  '': {  #DONE
                       'look': 'From the floor you cannot see anything on top of the COUNTER,+however you do see DRAPES hanging near the COUNTER.', 
                       'climb': 'What are you trying to CLIMB?',
                       'jump': 'You hop up and down like a bunny rabbit.',
                       'open': 'What are you trying to OPEN?',
                       'get': 'What are you trying to GET?',
                       'push': 'What are you trying to PUSH?',
                  },
                  'cabinet':{#DONE
                       'look': 'You remember that there is a CABINET on the COUNTER but you cannot see it from here.', 
                       'climb': 'You are not close enough to the CABINET to attempt to CLIMB it.',
                       'jump': 'You are not close enough to the CABINET to attempt to JUMP on it.',
                       'open': 'You are not close enough to the CABINET to attempt to OPEN it.',
                       'get': 'You are not close enough to the CABINET to attempt to GET it.',
                       'push': 'You are not close enough to the CABINET to attempt to PUSH it.',
                  },
                  'catnip': {#DONE
                       'look': 'You cannot see any CATNIP, but you know by the smell that there is CATNIP on the COUNTER.', 
                       'climb': 'You are not close enough to the CATNIP to attempt to CLIMB it.',
                       'jump': 'You are not close enough to the CATNIP to attempt to JUMP on it.',
                       'open': 'You are not close enough to the CATNIP to attempt to OPEN it.',
                       'get': 'You are not close enough to the CATNIP to attempt to GET it.',
                       'push': 'You are not close enough to the CATNIP to attempt to PUSH it.',
                  },
                  'claws': {#DONE
                        'look': {
                            'True': 'Your CLAWS are currently RETRACTed. Maybe you should EXTEND them.',
                            'False': 'Your CLAWS are currently EXTENDed. Perfect for CLIMBing.'
                        },
                        'climb': 'You cannot CLIMB your own CLAWS. That does not even make sense.',
                        'jump': 'You cannot JUMP your own CLAWS. That does not even make sense.',
                        'open': 'You cannot OPEN your own CLAWS. Perhaps you should LOOK at them.',
                        'get': 'You cannot GET your own CLAWS. That does not even make sense.',
                        'push': 'You cannot PUSH your own CLAWS. That does not even make sense.', 
                  },
                  'counter': {#DONE
                       'look': 'The counter is very tall, too tall to JUMP onto.+There are flowing DRAPES next to the COUNTER.+You see that the COUNTER top hangs over the sides.+You will not be able to CLIMB the COUNTER.', 
                       'climb': 'The COUNTER top hangs over the sides. You recognize that you cannot CLIMB the COUNTER.',
                       'jump': 'You attempt to JUMP onto the COUNTER but fail. You do not even make it halfway.',
                       'open': 'You cannot OPEN the COUNTER.',
                       'get': 'You cannot GET the COUNTER.',
                       'push': 'You strain your muscles as you PUSH against the COUNTER.+It does not budge at all. You feel winded and slightly silly.',
                  },
                  'drapes': {#DONE
                       'look': 'You see flowing DRAPES hanging next to the COUNTER.+The DRAPES reach from the ceiling to the floor.+Perhaps you can CLIMB them...', 
                       'climb': {
                            'True': 'You attempt to CLIMB but you can not grip the DRAPES with your soft pads.+Perhaps you should EXTEND your CLAWS.',
                            'False': 'With your sharp CLAWS you easily CLIMB the DRAPES.',
                        },
                       'jump': 'You cannot JUMP onto the DRAPES.+Perhaps there is a different COMMAND you can use to reach the top...',
                       'open': 'You cannot OPEN the DRAPES.',
                       'get': 'You grasp the DRAPES within your paws. They feel silky smooth.',
                       'push': 'You swat at the DRAPES. They sway harmlessly in front of your face.',
                  },
                  'nami': {#DONE
                       'look': 'You do not see NAMI from here.', 
                       'climb': 'You cannot CLIMB NAMI from here.',
                       'jump': 'You cannot JUMP on NAMI from here.',
                       'open': 'You cannot OPEN NAMI from here.',
                       'get': 'You cannot GET NAMI from here.',
                       'push': 'You cannot PUSH NAMI from here.',
                  },
}

outcome_drapes = {  #DONE
                  '': { #DONE
                       'look': 'The room looks different from up here. The COUNTER is below you. You can easily land on it with a JUMP.', 
                       'climb': 'You have already CLIMBED the DRAPES. You cannot safely CLIMB anything else.',
                       'jump': 'You carefully JUMP down onto the COUNTER.',
                       'open': 'You are hanging from the DRAPES. You cannot safely OPEN anything.',
                       'get': 'You are hanging from the DRAPES. You cannot safely GET anything.',
                       'push': 'You are hanging from the DRAPES. You cannot safely PUSH anything.'},
                  'cabinet':{ #DONE
                       'look': 'You can see a CABINET on the COUNTER top. Perhaps you should JUMP down to investigate further.', 
                       'climb': 'You are not close enough to the CABINET to attempt to CLIMB it.',
                       'jump': 'Your instincts tell you that you cannot safely JUMP towards the CABINET.',
                       'open': 'You are not close enough to the CABINET to attempt to OPEN it.',
                       'get': 'You are not close enough to the CABINET to attempt to GET it.',
                       'push': 'You are not close enough to the CABINET to attempt to PUSH it.',
                  },
                  'catnip': {#DONE
                       'look': 'The CATNIP smell is getting stronger, but you do not see it anywhere.', 
                       'climb': 'You are not close enough to the CATNIP to attempt to CLIMB it.',
                       'jump': 'You are not close enough to the CATNIP to attempt to JUMP on it.',
                       'open': 'You are not close enough to the CATNIP to attempt to OPEN it.',
                       'get': 'You are not close enough to the CATNIP to attempt to GET it.',
                       'push': 'You are not close enough to the CATNIP to attempt to PUSH it.',
                  },
                  'claws': {#DONE
                        'look': {
                            'True': '', #This results in an ending. Use outcome_endings instead
                            'False': 'Your CLAWS are currently EXTENDed. It might be dangerous to RETRACT them.'
                        },
                        'climb': 'You cannot CLIMB your own CLAWS. That doesn\'t even make sense.',
                        'jump': 'You cannot JUMP on your own CLAWS. That doesn\'t even make sense.',
                        'open': 'You cannot OPEN your own CLAWS.',
                        'get': 'You cannot GET your own CLAWS. That doesn\'t even make sense.',
                        'push': 'You cannot PUSH your own CLAWS. That doesn\'t even make sense.', 
                  },
                  'counter': { #DONE
                       'look': 'The COUNTER is just below you. You can easily use your cat reflexes to JUMP safely down.', 
                       'climb': 'You do not need to CLIMB the COUNTER. You are already above it.',
                       'jump': 'You carefully JUMP down onto the COUNTER.',
                       'open': 'You cannot OPEN the COUNTER.',
                       'get': 'You cannot GET the COUNTER.',
                       'push': 'You cannot PUSH the COUNTER.',
                  },
                  'drapes': {#DONE
                       'look': 'You are still gripping the DRAPES firmly beneath your CLAWS.', 
                       'climb': 'You do not need to CLIMB the DRAPES any higher. You are already above the COUNTER.',
                       'jump': 'You are already hanging from the DRAPES. You cannot JUMP on the DRAPES.',
                       'open': 'You cannot OPEN the DRAPES.',
                       'get': 'You cannot GET the DRAPES.',
                       'push': 'You PUSH the DRAPES. Nothing happens.',
                  },
                  'nami': { #DONE
                       'look': 'You do not see NAMI from here.', 
                       'climb': 'You cannot CLIMB NAMI from here.',
                       'jump': 'You cannot JUMP on NAMI from here.',
                       'open': 'You cannot OPEN NAMI from here.',
                       'get': 'You cannot GET NAMI from here.',
                       'push': 'You cannot PUSH NAMI from here.',
                  },
}

outcome_counter = {  #DONE 
                  '': { #DONE
                       'look': {
                           'True': 'From the COUNTER top you see an easily reachable CABINET.+With some guilt, you can see where the NAMI figurine used to stand.',
                           'False': 'From the COUNTER top you see an easily reachable CABINET.+There is also a NAMI figurine near the edge of the COUNTER.',
                       },
                       'climb': 'What are you trying to CLIMB?',
                       'jump': 'You hop up and down like a bunny rabbit.',
                       'open': 'What are you trying to OPEN?',
                       'get': 'What are you trying to GET?',
                       'push': 'What are you trying to PUSH?'},
                  'cabinet':{#DONE
                       'look': {
                           'True': 'The CABINET is open and you see a container of CATNIP sitting within reach.+You need to GET the CATNIP out of the kitchen.',
                           'False': 'The CABINET is closed but the smell of CATNIP wafts out.+Your instincts say you should OPEN the CABINET.',
                       },
                       'climb': 'You do not need to CLIMB the CABINET.',
                       'jump': 'You do not need to JUMP on the CABINET.',
                       'open': {
                           'True': 'The CABINET is already open.',
                           'False': 'You use your paws to OPEN the CABINET.+The smell of CATNIP is now incredible strong. ',
                       },
                       'get': 'You can not GET the CABINET.',
                       'push': 'You PUSH the CABINET. It is attached to the wall. It does not move.',
                  },
                  'catnip': {#DONE
                       'look': {
                           'True': 'You see the CATNIP container. It looks beautiful. You need to GET it out of the kitchen.',
                           'False': 'You do not see the CATNIP but you can smell that it is in the CABINET.'
                       }, 
                       'climb': {
                           'True': 'You should not CLIMB on the CATNIP here. Someone is coming. GET it out of the kitchen.',
                           'False': 'You cannot CLIMB on the CATNIP. It is behind the CABINET door.'
                       },
                       'jump': {
                           'True': 'You should not JUMP on the CATNIP here. Someone is coming. GET it out of the kitchen.',
                           'False': 'You cannot JUMP on the CATNIP. It is behind the CABINET door.'
                       },
                       'open': {
                           'True': 'You should not OPEN the CATNIP here. Someone is coming. GET it out of the kitchen.',
                           'False': 'You cannot OPEN the CATNIP. It is behind the CABINET door.'
                       },
                       'get': {
                           'True': '', ###This results in an ending. Use outcome_endings instead
                           'False': 'You cannot GET the CATNIP. It is behind the CABINET door.'
                       },
                       'push': {
                           'True': '', #This results in an ending. Use outcome_endings instead
                           'False': 'You cannot PUSH the CATNIP. It is behind the CABINET door.'
                       },
                  },
                  'claws': {#DONE
                        'look': {
                            'True': 'Your CLAWS are currently RETRACTed. You don\'t think you will need to use them anymore.',
                            'False': 'Your CLAWS are currently EXTENDed. You don\'t think you will need to use them anymore.'
                        },
                        'climb': 'You cannot CLIMB your own CLAWS. That doesn\'t even make sense.',
                        'jump': 'You cannot JUMP your own CLAWS. That doesn\'t even make sense.',
                        'open': 'You cannot OPEN your own CLAWS.',
                        'get': 'You cannot GET your own CLAWS. That doesn\'t even make sense.',
                        'push': 'You cannot PUSH your own CLAWS. That doesn\'t even make sense.', 
                  },
                  'counter': {#DONE
                       'look': {
                           'True': 'The smell of CATNIP is coming from the CABINET.+There is nothing else of interst on the COUNTER.',
                           'False': 'The smell of CATNIP is coming from the CABINET.+There is a NAMI figurine near the edge of the COUNTER.',
                       }, 
                       'climb': 'You are already on the COUNTER. You cannot CLIMB the COUNTER.',
                       'jump': 'You are already on the COUNTER. You cannot JUMP onto the COUNTER.',
                       'open': 'You cannot OPEN the COUNTER.',
                       'get': 'You cannot GET the COUNTER.',
                       'push': 'You cannot PUSH the COUNTER.',
                  },
                  'drapes': {#DONE
                       'look': 'You look at the DRAPES and fondly remember your perilous CLIMB.', 
                       'climb': 'You do not need to CLIMB the DRAPES. You need to GET the CATNIP.',
                       'jump': 'You do not need to JUMP on the DRAPES. You need to GET the CATNIP.',
                       'open': 'You cannot OPEN the DRAPES.',
                       'get': 'You grab the DRAPES and hold them.+After a second you release them and let out a sigh of satisfaction.',
                       'push': 'You PUSH the DRAPES. Nothing continues to happen.',
                  },
                  'nami': { #DONE
                       'look': {
                           'True': 'The NAMI figurine lies broken on the kitchen floor.+A part of you wonders if you should have done things differently...', 
                           'False': 'The NAMI figurine looks very well made. You feel conflicted.+Should you interact with NAMI or should you look for the CATNIP...',
                       }, 
                       'climb': {
                           'True': 'The NAMI figurine lies broken on the kitchen floor. You cannot CLIMB on the figurine anymore.', 
                           'False': 'You cannot CLIMB on NAMI...although it does have a certain charm.+Perhaps you can GET the figurine instead...',
                       },
                       'jump': {
                           'True': 'The NAMI figurine lies broken on the kitchen floor. You cannot JUMP on the figurine anymore.', 
                           'False': 'You cannot JUMP on NAMI...although it does have a certain charm.+Perhaps you can GET the figurine instead...',
                       },
                       'open': {
                           'True': 'The NAMI figurine lies broken on the kitchen floor. You cannot OPEN the figurine further.', 
                           'False': 'This is a game for all ages. You cannot OPEN the NAMI figurine.',
                       },
                       'get': {
                           'True': 'The NAMI figurine lies broken on the kitchen floor. You can no longer GET the figurine.', 
                           'False': '',#This results in an ending. Use outcome_endings instead
                       },
                       'push': {
                           'True': 'The NAMI figurine lies broken on the kitchen floor. You can not PUSH the figurine.', 
                           'False': 'With a mischevious grin you PUSH NAMI over the edge of the COUNTER.+It lands with a satisfying crash and breaks into pieces.+Ludwig will be sad.',
                       },
                  },
}

#define functions
def GetLocationText(location): 
    return text_location_dict.get(location)

#access the specific location dictionary to get the text response
def GetResponse(location, object, command): 
    response = ''
    loc = location
    global endings_screen
    global playing_screen
    global main_screen
    global nami_broken
    global cabinet_open
    global claws_retracted
    global timer
 
    #These commands give these responses anywhere in the program.
    if command == 'help':
        response = text_help
        return response, loc
    elif command == 'listcommands':
        response = text_listcommands
        return response, loc
    elif command == 'listobjects':
        response = text_listobjects
        return response, loc
    
    
    #These commands give these responses at a menu screen (main/credits/endings)
    if not playing_screen: #at the main screen, credits screen or endings screen
        if command == 'start' and object == '':
            loc = 'floor' #set initial location
            #reset game variables
            nami_broken = False
            cabinet_open = False 
            claws_retracted = True 
            timer = timer_init
            #set screen bools
            playing_screen = True
        elif command == 'endings': #open the endings menu screen
            response = '' #response is retrieved outside of this function by using the 'endings' location
            loc = 'endings'
        elif command == 'credits': #open the credits menu screen
            response = '+'.join(text_credits) 
            loc = 'credits'
        elif command == 'quit':
            loc = 'menu'
        else:
            response = ''
    else: # These commands give these responses while the game is started (playing_screen == True)
        if command == 'start':
            response = 'You have already started the game.'
        elif command == 'endings':
            response = 'You are in the game. Please QUIT to view the ENDINGS.'
        elif command == 'credits':
            response = 'You are in the game. Please QUIT to view the ENDINGS.'
        elif command == 'quit':
            response = text_quit
            loc = 'menu'
            playing_screen = False
        elif command == 'poop': #Ending
            response = outcome_endings[ending_poop]
            pygame.mixer.Sound.play(lose)  
            endings_achieved[ending_poop] = 'X'
            loc = 'menu'
            playing_screen = False
        elif command == 'extend':
            if object == 'claws':
                response = text_extend_claws[str(claws_retracted)]
                claws_retracted = False
            else:
                response = 'What are you trying to EXTEND? Your CLAWS perhaps?'
        elif command == 'retract':
            if object == 'claws':
                if location == 'drapes':
                    response = outcome_endings[ending_drapes]
                    pygame.mixer.Sound.play(lose)  
                    endings_achieved[ending_drapes] = 'X'
                    loc = 'menu'
                    playing_screen = False
                else:
                    response = text_retract_claws[str(claws_retracted)]
                claws_retracted = True
            else:
                response = 'What are you trying to RETRACT? Your CLAWS perhaps?'  
        else: #All other commands are location specific
            if location == 'floor':   #floor location outcomes
                if command == 'climb' and object == 'drapes':
                    response = outcome_floor[object][command][str(claws_retracted)]
                    if not claws_retracted: # move onto the next level
                        loc = 'drapes'
                elif command == 'look' and object == 'claws':
                    response = outcome_floor[object][command][str(claws_retracted)]
                else:
                    response = outcome_floor[object][command]
            elif location == 'drapes': #drapes location outcomes
                if command == 'jump' and (object == '' or object == 'counter'): #move onto the next level
                    response = outcome_drapes[object][command]
                    loc = 'counter'
                elif command == 'look' and object == 'claws':
                    response = outcome_drapes[object][command][str(claws_retracted)]
                else:
                    response = outcome_drapes[object][command]
            elif location == 'counter': #counter location outcomes. Makes more sense to check object first (3 game bools are relevant)
                if object == 'catnip':
                    if command == 'push':
                        if cabinet_open: #ENDING
                            response = outcome_endings[ending_lostcatnip]
                            pygame.mixer.Sound.play(lose)  
                            endings_achieved[ending_lostcatnip] = 'X'
                            loc = 'menu'
                            playing_screen = False
                        else:
                            response = outcome_counter[object][command][str(cabinet_open)]
                    elif command == 'get': 
                        if cabinet_open and nami_broken: #ENDING
                            response = outcome_endings[ending_escaped]
                            pygame.mixer.Sound.play(win)  
                            endings_achieved[ending_escaped] = 'X'
                            loc = 'menu'
                            playing_screen = False 
                        elif cabinet_open and not nami_broken: #ENDING
                            response = outcome_endings[ending_caught]
                            pygame.mixer.Sound.play(lose)  
                            endings_achieved[ending_caught] = 'X'
                            loc = 'menu'
                            playing_screen = False
                        else:
                            response = outcome_counter[object][command][str(cabinet_open)]
                    else:
                        response = outcome_counter[object][command][str(cabinet_open)]
                elif object == 'cabinet':
                    if command == 'look' or command == 'open':
                        response = outcome_counter[object][command][str(cabinet_open)]
                        if command == 'open' and not cabinet_open:
                            cabinet_open = True
                    else:
                        response = outcome_counter[object][command]                
                elif object == 'claws':
                    if command == 'look':
                        response = outcome_counter[object][command][str(claws_retracted)]
                    else:
                        response = outcome_counter[object][command]
                elif object == 'nami':
                    if command == 'get' and nami_broken is False: #ENDING
                        response = outcome_endings[ending_nami]
                        pygame.mixer.Sound.play(win)  
                        endings_achieved[ending_nami] = 'X'
                        loc = 'menu'
                        playing_screen = False
                    elif command == 'push' and nami_broken is False:
                        response = outcome_counter[object][command][str(nami_broken)]
                        nami_broken = True
                    else:
                        response = outcome_counter[object][command][str(nami_broken)]              
                elif command == 'look' and (object == 'counter' or object == ''):
                    response = outcome_counter[object][command][str(nami_broken)]  
                else: #object is 'drapes' or misc '' or misc 'counter'
                    response = outcome_counter[object][command]                 
                    
    return response, loc    

    #parse the user input to find the COMMAND, OBJECT, and correct RESPONSE,LOCATION
def CheckInput(user_text, location):
    x = user_text.lower().split()
    commandcount,objectcount,othercount = 0,0,0
    loc = location
    response = ''
    command = ''
    object = ''
    global timer
    
    for i in x:
        if i in commands:
            command = i
            commandcount += 1
        elif i in objects:
            object = i
            objectcount += 1
        else: #word is not in commands or objects
            othercount += 1
    
    #check commandcount and objectcount to determine correct response
    if commandcount == 0:
        response = 'No command entered. Please enter a command.'
    elif commandcount > 1:
        response = 'You are confused. Too many commands at once.'
    elif commandcount == 1 and (othercount > 0 or objectcount > 1):
        object = '' #Debug function block. Do not need object = 'other' for the actual game
        response, loc = GetResponse(location,object,command)    
    else:
        #looped over input and have 1 command and 1 object
        response, loc = GetResponse(location,object,command)       
    
    return response, loc
    

import sys, pygame, time
from pygame.locals import *

#initialize variables
text_user = ''
text_response = ''
text_location = ''
location = 'menu'
endings_screen = False
main_screen = True
playing_screen = False
#initialize game state bools
nami_broken = False
cabinet_open = False 
claws_retracted = True


pygame.init()
pygame.mixer.init()

#Define sound effects
win = pygame.mixer.Sound('sounds/andthewinneris_congusbongus.ogg')
lose = pygame.mixer.Sound('sounds/totalfail_congusbongus.ogg')
  

#get the resolution of the user and set the display resolution
design_res_x = 0.9*1920 #Design resolution
design_res_y = 0.9*1080

resolution_user = pygame.display.get_desktop_sizes()
user_res_x = 0.95*resolution_user[0][0]
user_res_y = 0.95*resolution_user[0][1]

#Set up User Window and Design Screen so I can scale them later
window = pygame.display.set_mode([user_res_x, user_res_y])
screen = pygame.Surface([design_res_x, design_res_y])


clock = pygame.time.Clock()

#initialize and set up the timer event
timer_init = 90
timer = timer_init
pygame.time.set_timer(pygame.USEREVENT, 1000)

#set the game title
title = "Get That Catnip Coots!"

#define Font info
Titlefont = pygame.font.Font('./fonts/Ac437_IBM_VGA_8x16.ttf', 60)
Labelfont = pygame.font.Font('./fonts/Ac437_IBM_VGA_8x16.ttf', 40) 
Textfont = pygame.font.Font('./fonts/Ac437_IBM_VGA_8x16.ttf', 30) 


line_height = design_res_y*0.04 #space between lines
white = (255, 255, 255)
black = (0, 0, 0)

is_running = True

#Game loop begins
while is_running:
    
    screen.fill(black)
    center_screen = screen.get_rect().center
    center_x = center_screen[0]
    center_y = center_screen[1]
    
    if not playing_screen:
        #print to screen the Title
        # TITLE 
        title_y = 0.07*design_res_y
        title_img = Titlefont.render(title, True, white)
        screen.blit(title_img, title_img.get_rect(center = (center_x,title_y))) 
    else:
        #print to screen the current location (if not in a menu screen)   
        #CURRENT LOCATION
        loc_x = design_res_x*.85
        loc_y = design_res_y*.1
        locationLabel_img = Labelfont.render("Location:", True, white)
        location_img = Labelfont.render(location.capitalize(), True, white)
        locationLabel_img_center = locationLabel_img.get_rect().center
        screen.blit(locationLabel_img, (loc_x, loc_y)) 
        screen.blit(location_img, locationLabel_img.get_rect(center = (loc_x+locationLabel_img_center[0], loc_y+0.07*design_res_y)))
        
        #print the timer to the screen (if not in a menu screen)
        # TIMER
        timerlabel = Labelfont.render('Time:', True, white)
        timer_str = Labelfont.render(str(timer), True, white)
        timer_x = design_res_x*.05
        timer_y = design_res_y*.1
        screen.blit(timerlabel, (timer_x, timer_y))
        screen.blit(timer_str, (timer_x+0.01*design_res_x, timer_y+0.05*design_res_y))
    
    #print location text to screen
    #TEXT LOCATION
    text_location = GetLocationText(location)
    try:
        loc_response = text_location.split('+')
    except:
        loc_response = ['']
    for i in range(len(loc_response)):
        y = 0.17*design_res_y+line_height*i
        location_text_img = Textfont.render(loc_response[i], True, white)
        screen.blit(location_text_img, location_text_img.get_rect(center = (center_x, y)))
        
        
    
    #check if timer ran out and ending was reached       
    if timer == 0:
        text_response = outcome_endings[ending_timer]
        pygame.mixer.Sound.play(lose)  
        endings_achieved[ending_timer] = 'X'
        playing_screen = False
        timer = timer_init   
    
    #draw rectangle around user input position
    #INPUT BOX
    inputbox = Rect(design_res_x*.03, design_res_y*.885,design_res_x*.94,design_res_y*.075) #RECT(Left,Top,Width,Height)
    pygame.draw.rect(screen,white,inputbox,5,5)
    
    #print to screen the user input
    #USER INPUT TEXT
    user_x = design_res_x*0.05 
    user_y = design_res_y*.907 
    text_user_img = Textfont.render(text_user, True, white)
    screen.blit(text_user_img, (user_x, user_y))
    
    #Draw user input symbol
    #USER INPUT SYMBOL '>'
    screen.blit(Textfont.render('>', True, white), (user_x*.78, user_y))
    
    #Draw blinking cursor around user input position
    #USER BLINKING CURSOR
    cursor_rect = text_user_img.get_rect()
    cursor_rect.topleft = (user_x,user_y)
    cursor = pygame.Rect(cursor_rect.topright, (2, cursor_rect.height))
    if time.time() % 1 > 0.6:
        pygame.draw.rect(screen, white, cursor)
    
    #print to screen the response from the user input
    # RESPONSE TEXT 
    response_x = ending_x1 = design_res_x*0.05
    response_y = ending_y1 = design_res_y*0.50
    ending_x2 = design_res_x*0.4
    ending_y2 = ending_y1*1.1
    ending_y3 = ending_y1*1.2
    ending_y4 = ending_y1*1.3

    if location == 'endings':
        #Print endings screen
        screen.blit(Textfont.render(text_ending[0]+'['+endings_achieved[0]+']', True, white), (ending_x1, ending_y1))
        screen.blit(Textfont.render(text_ending[1]+'['+endings_achieved[1]+']', True, white), (ending_x2, ending_y1))
        screen.blit(Textfont.render(text_ending[2]+'['+endings_achieved[2]+']', True, white), (ending_x1, ending_y2))
        screen.blit(Textfont.render(text_ending[3]+'['+endings_achieved[3]+']', True, white), (ending_x2, ending_y2))
        screen.blit(Textfont.render(text_ending[4]+'['+endings_achieved[4]+']', True, white), (ending_x1, ending_y3))
        screen.blit(Textfont.render(text_ending[5]+'['+endings_achieved[5]+']', True, white), (ending_x2, ending_y3))
        screen.blit(Textfont.render(text_ending[6]+'['+endings_achieved[6]+']', True, white), (ending_x1, ending_y4))
    else:
        try:
            response = text_response.split('+')
        except:
            response = ['']
        for i in range(len(response)):
            y = response_y+line_height*i
            screen.blit(Textfont.render(response[i], True, white), (response_x, y))
    
    
    #Draw LINE TO SPLIT LOCATION TEXT FROM RESPONSE TEXT
    line_x_start = design_res_x*.03
    line_x_end = design_res_x*.97
    line_y_start = line_y_end = design_res_y*.44

    pygame.draw.line(screen,white,(line_x_start,line_y_start),(line_x_end,line_y_end),5)
    
    #update the screen and in-game clock
    frame = pygame.transform.scale(screen, (user_res_x, user_res_y)) #scale the design screen to fit the user frame
    window.blit(frame, frame.get_rect())
    pygame.display.flip()
    clock.tick(60)
    pygame.display.update()
    
    
    #check pygame events
    for event in pygame.event.get():
                
        if event.type == pygame.QUIT:
            pygame.quit()
            is_running = False
        
        if event.type == pygame.KEYDOWN:
            #check for backspace key
            if event.key == pygame.K_BACKSPACE:
                text_user = text_user[:-1]
            
            #check for return key
            elif event.key == pygame.K_RETURN:
                if text_user.lower() == 'exit':
                    pygame.quit()
                    is_running = False
                text_response, location = CheckInput(text_user,location)
                text_user = ''
                
            #add the key to the user string
            else:
                text_user += event.unicode
        
        #increments the timer if the game is running (playing_screen == True)          
        if event.type == pygame.USEREVENT:
            if playing_screen:
                timer -= 1


#end program    
pygame.display.quit()
pygame.quit()
sys.exit()