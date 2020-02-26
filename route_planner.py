from tkinter import Button,Tk,Label,Checkbutton,Listbox,IntVar,Toplevel,messagebox,Grid,LEFT,END,Scrollbar,ACTIVE
import matplotlib.pyplot as plt

from PIL import Image, ImageTk

import sys
import os
import json
import numpy as np


""" DEFAULT SETTINGS """

def default_settings():
    return '0101011'

""" INITIALISE FILES """

def checkFiles():

    def writeSettings():
        with open(settings,'w') as f:
            f.write(default_settings())

    myIslands = getPath('Islands/my_islands.txt')
    if not os.path.isfile(myIslands):
        open(myIslands, 'a').close()

    settings = getPath('Islands/settings.set')
    if not os.path.isfile(settings):
        writeSettings()
    else:
        with open(settings,'r') as f:
            lines = f.read()
        if len(lines) != len(default_settings()):
            writeSettings()
            

""" PYTHAG THEOROM SHORTEST ROUTE """

def pyThag(x1, y1, x2, y2):
    a = (float(x2)-float(x1)) #a = difference in x
    b = (float(y2)-float(y1)) #b = difference in y
    return (a**2+b**2)**(1/2) #c = sqrt(a^2 + b^2)


""" READ ISLAND FILE """

def getIslands(file = 'all_islands.json'):
    path = getPath('Islands/'+file)
    try:
        with open(path, 'r') as f:
            islands = json.load(f)
        return islands
    except:
        close(1, file) #error code 1: file does not exist


""" READ SETTINGS """

def readSettings():
    def openSettings():
        path = getPath('Islands/settings.set')
        with open(path, 'r') as f:
            settings = f.read()
        if len(settings)!=0:
            return settings
        else:
            return default_settings()
    
    try:
        return openSettings()
    except:
        close(2)    #error code 2: if settings file does not exist inform user that customisation will have been reset
        checkFiles()#add and write into the file default settings
        return openSettings()


""" CHECK SETTINGS """

def checkSettings(setting_id):
    settings = readSettings()
    if settings[setting_id] == '1':
        return True
    return False


""" GET ABSOLUTE PATH """

def getPath(relativePath):
    try:
        currentLocation = os.path.dirname(__file__)                 #get absolute current location
        absolutePath = os.path.join(currentLocation, relativePath)  #get absolute path to desired file
        return absolutePath
    except:
        close(1, relativePath) #error code 1: path is incorrect

""" COLOUR THEME """

global bg,fg,base
dark = checkSettings(6)
if dark: #use dark theme
    bg =  '#2d2d2d'
    fg = '#cccccc'
    base = '#111111'
else: #use blue theme
    bg = '#244447'
    fg = '#cccccc'
    base = '#1a3538'

""" WIDTH IMAGE FORMATTING """

def FormatImage(path, width=None, height=None):
    imgPath = getPath('Images/'+path)
    img = Image.open(imgPath)
    
    if width == None:
        width = img.size[0]
    if height == None:
        height = img.size[1]
        
    return ImageTk.PhotoImage(img.resize((width, height), Image.ANTIALIAS))
    
        
""" BUTTONS THAT CHANGE COLOUR WHEN YOU CLICK """

class HoverButton(Button):
    def __init(self, master, **kw):
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

""" TOOL TIPS FOR ANY WIDGET """
""" CREDIT: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter """

class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

        
""" SETTINGS WINDOW """

def open_settings():
    class settings_window:
        def __init__(self, master):
            #master.iconbitmap(getPath('seaofthievesicon_YaU_icon.ico'))
            master.title('Settings')
            master.configure(background = bg)
            master.grab_set()

            #Settings Label
            self.title_img = FormatImage('settings.png',260,50)
            Label(master, image=self.title_img, bg=bg).grid(column=0, row=0, pady=10, sticky='W')

            #get settings
            settings = readSettings()

            #2d list of checkbox title, tooltip info for each setting checbox
            checkBoxInfo = [['End at Outpost','If there is an outposts on your voyage, it will be saved until the end of the voyage. WARNING: This may increase voyage time. Alternatively you can use the \'Nearest Port\' feature at the end of the voyage.'],
                            ['Quick Search', 'Use the DEFAULT \'Next Nearest Node\' algorithm. This may not always be shortest journey. RECOMENDED ON. Off, uses an \'Absolute Shortest Journey\' algorithm. This can cause long wait times for long voyages'],
                            ['Visit a Seapost on Route', 'Visit a seapost at some point on your voyage. Seapost will be fit in for minimal impact on journey time. WARNING: NOT RECOMENED WITH QUICK SEARCH OFF.'],
                            ['Display Nearest Fort in Nearest Port','When finding the nearest Outpost or nearest Seapost using \'Voyage to Your Nearest Port\', display your nearest Fortress.'],
                            ['Visit Islands in Order','When planning the voyage to multiple islands, The journey will be plotted in the order specified. WARNING: This will override all other settings related to planning your main voyage.'],
                            ['Keep All Journies Open','When a voyage is loaded, all maps will remain open. If disabled, only 1 map will be open at a given time'],
                            ['Dark Theme','When enabled the theme is gray and black. If enabled it will use shades of blue. NOTE: only activates after RESTART']]

            self.cbVars = [] #list of the variables for each checkbox
            
            for i, text in enumerate(checkBoxInfo):
                self.cbVar = IntVar()           #initialise variable for checkbox
                self.cbVar.set(settings[i])     #set setting variable to the value in the settings file
                self.cbVars.append(self.cbVar)  #add value to list of values
                self.cb = Checkbutton(master, text=text[0], font = 12, bg=bg, fg=fg, selectcolor=base, justify=LEFT,variable = self.cbVar, onvalue=1, offvalue=0)
                self.cb.grid(row=i+1, column=0, sticky='w', padx=5)
                self.cbtt = CreateToolTip(self.cb, text[1]) #assign tooltip to checkbox

          
        def confirmSettings(self):
            #get settings from checkboxes
            settings = [str(i.get()) for i in self.cbVars]
            
            proceed=True #assume user is okay with using/not using quick search
            if settings[1] == '0': #check the user is okay with not using quick search
                proceed = messagebox.askyesno('Warning', 'Are you sure you want to disable \'Quick Search\'.\nVoyages will take a while to compute.',icon = 'warning', parent=master)
                if not proceed: #if the user changes their mind don't close settings and reset the corresponding checkbox
                    self.cbVars[1].set(1)
                    return False

            if settings[4] == '1': #check the user is okay with not using quick search
                proceed = messagebox.askyesno('Warning', 'Are you sure you want to visit islands in order? This will override all other related settings.',icon = 'warning', parent=master)
                if not proceed: #if the user changes their mind don't close settings and reset the corresponding checkbox
                    self.cbVars[4].set(1)
                    return False

            if proceed: #if the user is happy with quick search check they want to save the other settings
                save = messagebox.askyesno('Are you sure?', 'Do you want to save any changes to your settings?', parent=master)
                if save:
                    path = getPath('Islands/settings.set')
                    with open(path, 'w') as f:
                        f.write(''.join(settings)) #write out each setting as a 1/0 string (no spaces)
            return True


        def closeSettings(self):
            confirm = self.confirmSettings()
            if confirm: #confirmSettings returns a boolean to proceed in closing window or not
                master.grab_release()
                master.destroy()
            
            
    master = Toplevel()
    settings_window = settings_window(master)
    master.resizable(width=False, height=False) #don't all resize
    master.protocol('WM_DELETE_WINDOW', settings_window.closeSettings)
    master.mainloop()


""" VOYAGE PLANNER WINDOW """

def plan_voyage(mode):
    class plan_window:
        def __init__(self, master):
            self.master = master
            #master.iconbitmap(getPath('seaofthievesicon_YaU_icon.ico'))
            master.title('Plan Your Voyage')
            master.configure(background = bg)
            master.grab_set()
            
            islands = getIslands() #get dictionary of island names : coordinates

            #Sea of thieves logo as title
            self.title_img = FormatImage('plan_voyage.png', 235, 90)# original 400x180
            Label(master, image=self.title_img, bg=bg).grid(column=0, row=0, sticky='W', columnspan=2)

            #Listbox of all islands in alphabetical order
            self.listAll = Listbox(master, font = ('Ariel',14), fg=fg, bg=base, highlightbackground=base, height=18)
            self.listAll.grid(column=0, row=1, sticky='EW')

            islands = sorted(islands.keys())
            for i in islands:
                self.listAll.insert(END, i) #could use #.title

            #Add scroll bar to the listbox
            self.scrollAll = Scrollbar(master, orient='vertical', command = self.listAll.yview)
            self.scrollAll.grid(row=1, column=1, sticky='NS')
            #Setup listbox with scrollbar
            self.listAll.config(yscrollcommand=self.scrollAll.set)

            if mode == 1:
                #inform user that first island will be start position
                self.plan_info = FormatImage('plan_info.png', 225, 75) #original = 450x180
                Label(master, image=self.plan_info, bg=bg).grid(column=2, row=0, sticky='NE', columnspan=2, padx=5, pady=5)

                #Listbox of selected islands to visit
                self.listSelected = Listbox(master, font = ('Ariel',14), fg=fg, bg=base, highlightbackground=base, height=18)
                self.listSelected.grid(column=2, row=1, stick='EW')

                #Add scroll bar to the listbox
                self.scrollSelected = Scrollbar(master, orient='vertical', command = self.listSelected.yview)
                self.scrollSelected.grid(row=1, column=3, sticky='NS')
                #Setup listbox with scrollbar
                self.listSelected.config(yscrollcommand=self.scrollSelected.set)

                #Images for Buttons
                self.addimg = FormatImage('add.png', 235,50)
                self.removeimg = FormatImage('remove.png', 235,50)
                self.loadimg = FormatImage('load.png', 235,50)

                #Buttons
                self.add = HoverButton(master, image=self.addimg, command = self.addIsland, bg=bg, fg=fg, activebackground=bg, bd=0).grid(column=0, row=2, columnspan=2, sticky='EW', pady=5)
                self.remove = HoverButton(master, image=self.removeimg, command = self.removeIsland, bg=bg, fg=fg, activebackground=bg, bd=0).grid(column=2, row=2, columnspan=2, sticky='EW')
                self.load = HoverButton(master, image=self.loadimg, command  = self.loadPrev, bg=bg, fg=fg, activebackground=bg, bd=0).grid(column=2, row=3, columnspan=2, sticky='EW', pady=5)

            
            self.confirmimg = FormatImage('confirm.png', 235,50)
            self.confirm = HoverButton(master, image=self.confirmimg, command = self.loadVoyage, bg=bg, fg=fg, activebackground=bg, bd=0).grid(column=0, row=3, columnspan=2, sticky='EW', pady=5)


        def addIsland(self):
            #add island from listbox of all islands to listbox of islands to visit
            island = self.listAll.get(ACTIVE)
            self.listSelected.insert(END, island)


        def removeIsland(self):
            #remove island from listbox containing islands to visit
            self.listSelected.delete(ACTIVE)


        def loadPrev(self):
            try:
                path = getPath('Islands/my_islands.txt')
                with open(path, 'r') as f: #get islands as a list sa order matters. First island is start position
                    islands = f.read()

                    #if the file of previosu voyage is empty tell user there is no previous voyage
                    if len(islands)==0:
                        raise Exception

                    result = messagebox.askyesno("Last Voyage", "Would you like to load your last voyage?\n\n"+islands, parent=self.master)
                    #if user wants to load voyage, load list of islands into listbox of islands to visit
                    if result:
                        islands = islands.split('\n') #split islands into a list of names
                        #Add Islands to Listbox
                        for i in islands:
                            self.listSelected.insert(END, i)
            
            except: #if there is no file of a previous voyage inform user that there is no previous voyae
                messagebox.showerror('Error','There is no previous voyage to load', parent=self.master)


        """
        LOAD THE VOYAGE AND CALL OUTPUT OF MAP
        """

        def loadVoyage(self):
            
            if mode == 1: #mode 1: multiple Island Voyage

                """
                READ IN ALL THE ISLANDS SELECTED BY USER
                """
                
                try:
                    #tuple of all islands in list. If there is nothing an exception will be raised
                    islands = self.listSelected.get(0, END)
                    if len(islands)==0:
                        raise Exception
                    else:
                        #remove duplicate islands
                        unique = []
                        [unique.append(i) for i in islands if i not in unique]

                        path = getPath('Islands/my_islands.txt')
                        with open(path, 'w') as f:
                            f.write(('\n').join(unique))#join to write to file

                except Exception: #if no islands have been selected an error is raised
                    messagebox.showerror('Error','No islands have been selected. Choose some islands to visit before setting on a voyage', parent=self.master)
                    return

                """
                CALCULATE THE JOURNEY
                """

                #Load setting 5: is the journey in the order the user wants?
                #Load setting 2: does the user want to find the absolute shortest journey?
                #Load setting 3: does the user want to visit an seapost on route?
                defaultOrder = checkSettings(4)
                quick = checkSettings(1)
                seapost = checkSettings(2)
                
                if not defaultOrder:#see if user wants to plot voyage in order they add them
                    if not seapost: #see if seapost is to be visited on journey
                        if quick:   #see if using the nearest node algorithm
                            route = quick_sj()
                    
                        else:       #see if using the absolute shortest journey algorithm)
                            route = absolute_sj()

                    else: #sea if user wants to visit a seapost at somepoint during their jouney
                        seaposts = getIslands('seaposts.json') #Read in a diction of seaposts : [x coordinate, ycoordinate]
                        
                        #check if a seapost is already in the list of islands to visit
                        exist = False
                        for seapost in seaposts: #iterate through all seaposts
                            if seapost in unique:#check if seapost is in islands to visit
                                exist = True
                                break

                        if exist:#if user already plans to visit seapost, ignore and run route normally
                            if quick:   #see if using the nearest node algorithm
                                route = quick_sj()
                    
                            else:       #see if using the absolute shortest journey algorithm)
                                route = absolute_sj()
        
                        else:    #if user isn't already visiting a seapost,
                                 #loop through all seaposts to find shortest journey
                            shortest=[]
                            for seapost in seaposts:
                                if quick:   #see if using the nearest node algorithm
                        
                                    voyage = quick_sj(seapost)   #find shortest journey but with an added seapost
                                    if len(shortest) == 0:        #check if the shortest journey so far has any voyages to compare with
                                        shortest = voyage        #set shortest to the current voyage
                                    elif voyage[1] < shortest[1]:#if the current voyage is less than the shortest voyage so far
                                        shortest = voyage        #set shortest to current voyage
                                    
                                else: #see if using the absolute shortest journey algorithm)
                                    voyage = absolute_sj(seapost)
                                    if len(shortest) == 0:        #check if the shortest journey so far has any voyages to compare with
                                        shortest = voyage        #set shortest to the current voyage
                                    elif voyage[1] < shortest[1]:#if the current voyage is less than the shortest voyage so far
                                        shortest = voyage        #set shortest to current voyage
                                    
                            #find seapost in disatnces with lowest journey time
                            #set the route to journey with the shortest distance
                            route = shortest


                else:   #display voyage in order it was set by user
                    try:
                        path = getPath('Islands/my_islands.txt')
                        with open(path, 'r') as f: #get islands as a list sa order matters. First island is start position
                            myIslands = f.read()
                            myIslands = myIslands.split('\n')
                        route = (myIslands,0) #later expects a distance to remove
                    except:
                        route = None

                    
            elif mode == 2: #mode 2: nearest ports
                current = self.listAll.get(ACTIVE) #get users current island from selected island from listbox
                route = nearest_ports(current)
                
             #if nothing is returned from shortest journey raise error that file is missing
            #if not None, route = ([island names], distance_of_journey)
            if route != None:
                create_map(route[0], mode) #get journey info, ignore distance
                
            #route may = None if a file is deleted during the mapping process
            else:
                messagebox.showerror('Error','An unexpected error has occured. Please try again. If this message persists please restart the program.', parent=self.master)


        def closePlan(self):
            master.grab_release()
            master.destroy()
            

    master = Toplevel()
    plan_window = plan_window(master)
    master.resizable(width=False, height=False) #don't all resize
    master.protocol('WM_DELETE_WINDOW', plan_window.closePlan)
    master.mainloop()


""" QUICK SHORTEST JOURNEY """

def quick_sj(port = None):
    try:
        path = getPath('Islands/my_islands.txt')
        with open(path, 'r') as f: #get islands as a list sa order matters. First island is start position
            myIslands = f.read()
            myIslands = myIslands.split('\n')
    except:
        return

    #IF THE USER IS WANTING TO VISIT PORT MID JOURNEY THIS ALGORITHM IS RUN THROUGH A LOOP
    #AND EACH PORT IS USED IN TURN.
    if port != None: 
        myIslands.append(port)

    saveOutpost = checkSettings(0) #check if in the settings it says to save outpost till end
    allIslands = getIslands() #get dictionary of island names : coordinates to find each islands coordinates
    myIslands = [i for i in myIslands if i in allIslands.keys()] # remove any invalid islands if people edit the myislands file manually

    i1 = myIslands[0]       #current island
    x1 = allIslands[i1][0]  #current island x
    y1 = allIslands[i1][1]  #current island y

    totalDistance = 0
    voyage = [i1] #voyage begins at current island contains list of names of islands

    for i in range(len(myIslands)-1):   #loop through the number of islands to be visited
        distances = {}  #dictionary used to store the distances to all other islands

        for island in myIslands: #loop through all islands to be visited to find nearest one
            i2 = island

            if i2 not in voyage and i2 != i1: #check the island hasn't already been visited
                
                x2 = allIslands[i2][0] #island x coordinate
                y2 = allIslands[i2][1] #island y coordinate

                distance = pyThag(x1,y1,x2,y2) #get distance to island
                distances[i2] = (distance)

        nearest = min(distances.keys(), key=lambda k:distances[k]) #find the island with the shortest distance
        
        #if the setting is enabled, save outpost until the end of the voyage
        if saveOutpost:
            outposts = len([i for i in distances if 'Outpost' in i]) #find if there are any outposts on the voyage

            #if the nearest island is an outpost and and theres only 1 outpost left in the voyage, save it till last, choose next closest island
            if len(distances) > 1 and 'Outpost' in nearest and outposts == 1:
                del distances[nearest]
                nearest = min(distances.keys(), key=lambda k:distances[k]) #find the island with the next shortest distance        

        totalDistance += distances[nearest] #find distance for total journey time
        
        i1,x1,y1 = nearest, allIslands[nearest][0], allIslands[nearest][1] #set current island to the nearest island
        voyage.append(i1) #update the voyage
    
    return voyage, totalDistance
        

""" ABSOLUTE SHORTEST JOURNEY """

### CALCULATOR FOR SHORTEST ROUTE BY FINDING EVERY POSSIBLE ROUTE AND CORRESPONDING TOTAL DISTANCE ###
def calc_all_routes(islandCoords, visit): 
    #island coords is dictionary of island names and coords
    #visit is list of islands to visit
    #these were kept seperate as order matters

    #define start island and distance to start island
    distances = [0]       #time structure:   [time1, time2]
    voyage = [[visit[0]]] #voyage structure: [[island 1, island 2, island 3],
    #                                         [island 1, island 3, island 2]]

    #base case saying if theres only 1 left in visits we are already here return the distance
    if len(visit) <= 1:
        return distances, voyage

    #loop through all islands besides start island to find all possible routes
    #from start island.
    #each recursive call will set the start island to visit[i] in the previous function call

    #each recursive call would create a new layer and each loop would create a new branch:

    #           island_1                         _____________island_1____________
    #          /        \                       /                |                \
    #     island_2     island_3           island_2            island_3           island_4
    #       /              \              /     |           /        \            |      \
    #   island_3        island_2     island_3  island_4   island_2  island_4   island_2  island_3
    #                                   |        |          |           |        |          |
    #                                island_4  island_3   island_4  island_2   island_3  island_2

    for i in range(1, len(visit[1:])+1):
        
        #distance between start island (visit[0]) and current loop island (visit[i])
        distance = pyThag(float(islandCoords[visit[0]][0]), float(islandCoords[visit[0]][1]),
                          float(islandCoords[visit[i]][0]), float(islandCoords[visit[i]][1]))
        
        otherVisit = [visit[i]]+visit[1:i]+visit[i+1:]
        subVoyage = calc_all_routes(islandCoords, otherVisit)

        #each loop check there is enough room in the voyage. used on the smaller branches
        if len(voyage) < i:
            voyage.append([visit[0]])

        if len(distances) < i:
            distances.append(0)

        #loop through all possible routes from the previous recursive call
        for j in range(len(subVoyage[1])):

            #if the last item in voyage is the length of a completed route
                #try concatonate the previous voyage with the voyage from the jth last recursive call.
                #   and add to the total value
                #if there are more possible voyages from the recursive call than in the voyage list, append this to as a new route in the voyage and a new distance for this new route
            #else an error is raised and and append as new route in the voyage and a new distance for this new route

            try:
                if len(voyage[-1])==len(visit):
                    raise Exception
                voyage[len(voyage)-1+j] = voyage[len(voyage)-1+j]+subVoyage[1][j]
                distances[len(distances)-1+j] += distance+subVoyage[0][j]
            except:
                voyage.append([visit[0]]+subVoyage[1][j])
                distances.append(distance+subVoyage[0][j])
    
    return distances, voyage

### CONTROLLER WHICH TAKES RESULTS FROM SHORTEST JOURNEY CALCULATOR ##
def absolute_sj(port=None):

    try:
        path = getPath('Islands/my_islands.txt')
        with open(path, 'r') as f: #get islands as a list sa order matters. First island is start position
            myIslands = f.read()
            myIslands = myIslands.split('\n')
    except:
        return

    if port != None: 
        myIslands.append(port)

    saveOutpost = checkSettings(0) #check if in the settings it says to save outpost till end
    allIslands = getIslands() #get dictionary of island names : coordinates to find each islands coordinates
    myIslands = [i for i in myIslands if i in allIslands.keys()] # remove any invalid islands if people edit the myislands file manually

    islandCoords = {i:allIslands[i] for i in myIslands} #get smaller dictionary only containing the islands and coords of places to visits
    routes = calc_all_routes(islandCoords, myIslands)   #get all possible routes

    fastest = routes[0].index(min(routes[0]))
    voyage = routes[1][fastest], routes[0][fastest] #set the voyage to the fastest route and corresponding distance

    shortest = []
    if saveOutpost:
        outposts = len([i for i in myIslands if 'Outpost' in i]) #find if there are any outposts on the voyage
        
        if outposts >= 1: #check the journey contains an outpost, loop until you find the shortest journey that ends in an outpost
            for i in range(len(routes[1])): #loop through all journeys
                if 'Outpost' in routes[1][i][-1]: #if the journey ends in an outpost

                    if len(shortest) == 0:                      #check if the shortest journey so far has any voyages to compare with
                        shortest = routes[1][i],routes[0][i]    #set shortest to the current voyage
                    elif routes[0][i] < shortest[1]:               #if the current voyage is less than the shortest voyage so far
                        shortest = routes[1][i],routes[0][i]    #set shortest to the current voyage

            voyage = shortest #set voyage to the fastest route that ends in an outpost and corresponding journey time
    return voyage #return list of voyages and distance


""" NEAREST PORT """

def nearest_ports(current):

    #shortest path
    def find_nearest(file,x1,y1):
        ports = getIslands(file) #get dictionary of island names : coordinates
        
        distances = {} #dictionary of distances to each port

        for port in ports: #find the distance to every port

            x2 = ports[port][0] #port x coordinate
            y2 = ports[port][1] #port y coordinate

            distance = pyThag(x1,y1,x2,y2)
            distances[port] = distance

        nearest = min(distances.keys(), key = lambda k: distances[k]) #find closest port
        return nearest #return the name of the port


    showFort = checkSettings(3) #check if in the settings it says to display forts
    allIslands = getIslands() #get dictionary of island names : coordinates to find current island coordinates

    x1 = allIslands[current][0]  #current island x
    y1 = allIslands[current][1]  #current island y

    #find each closest port
    outpost = find_nearest('outposts.json', x1, y1)
    seapost = find_nearest('seaposts.json', x1, y1)
    if showFort: #if setting enabled find closest fort
        fort = find_nearest('forts.json', x1, y1)

    #return list of closest ports
        return [current, outpost, seapost, fort],0 #function that calls for voyage expects a distance variable
                
    return [current, outpost, seapost],0 #function that calls for voyage expects a distance variable


""" CREATE MAP TO DISPLAY JOURNEY """

def create_map(route, mode):
    
    """
    SET UP JOURNEY PLOT AND AXIS
    """
    maps = checkSettings(5) #check if user wants only one map to be open at a given time
    if not maps:
        plt.close()
        
    plt.rcParams["figure.facecolor"] = bg #set background colour
    
    #Configure Axis
    fig, ax = plt.subplots()
    
    ax.set_ylim(26, 1)  #order of tick marks (1 at top 26 at bottom)
    ax.set_xlim(1, 26)  #order of tick marks x axis
    ax.xaxis.tick_top() #put axis tick marks at top of plot
                        #set x axis to letters not numbers. relate to game
    ax.set_xticklabels(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
                        'P','Q','R','S','T','U','V','W','X','Y','Z'])

    #colour axis tick marks
    ax.spines['bottom'].set_color(fg)
    ax.spines['top'].set_color(fg)
    ax.spines['left'].set_color(fg)
    ax.spines['right'].set_color(fg)
    for t in ax.xaxis.get_ticklines(): t.set_color(fg)
    for t in ax.yaxis.get_ticklines(): t.set_color(fg)
    
    #tick marks with labels along each axis
    plt.xticks(np.arange(1, 27, 1.0), color = fg)
    plt.yticks(np.arange(1, 27, 1.0), color = fg)
    
    #grid connecting all tick markers
    plt.grid()
    
    #map background
    path = getPath('Images/map_background.png')
    ax.imshow(plt.imread(path), aspect='auto', extent=(1,26,26,1), alpha=0.9, zorder=-1)

    """
    DISPLAY ISLANDS ON MAP
    """
    
    allIslands = getIslands() #dictionary of all islands
    #x coordinates for all islands
    #y coordinates for all islands
    xVals = [float(allIslands[i][0]) for i in allIslands]
    yVals = [float(allIslands[i][1]) for i in allIslands]
    
    #scatter plot each island
    plt.scatter(xVals, yVals, color = '#1b3816', zorder=3)

    """
    DISPLAY ROUTE ON MAP
    """
    
    #x coordinates of all islands on voyage
    #y coordinates of all islands on voyage
    xVals = [float(allIslands[i][0]) for i in route]
    yVals = [float(allIslands[i][1]) for i in route]
    
    if mode == 1: #Plot a multi island voyage
        plt.plot(xVals, yVals, ls='--')         #Plot route, x against y coords
        for i in range(len(route)):
            ax.annotate(route[i], xy=(xVals[i]-0.5, yVals[i]-0.2)) #place island name at each island

    
    else: #Plot the route to all nearest ports
        current = route[0]          #current island
        x1 = xVals[0]   #current island x coordinate
        y1 = yVals[0]   #current island y coordinate
        ax.annotate(current, xy=(x1-0.5, y1-0.2)) #place text at start island
        
        color = '#1f77b4'
        for i in range(len(route[1:])): #iterate through all nearest ports
            if i == 2:
                color = 'red'

            x2 = xVals[i+1]
            y2 = yVals[i+1]
            plt.plot([x1,x2], [y1,y2],color=color, ls='--')
            ax.annotate(route[i+1], xy=(x2-0.5, y2-0.2)) #place text at each island

    plt.show() #Show Voyage
    

""" STARTUP PARENT WINDOW """

class main_window:
    def __init__(self, master):
        self.master = master
        master.iconbitmap(getPath('seaofthievesicon_YaU_icon.ico'))
        master.title('Main Menu')  #window title
        master.configure(background = bg)  #background colour

        #Alternate title
        self.logo = FormatImage('logo2.png')
        Label(master, image=self.logo, bg=bg).grid(column=0, row=0, sticky='W',pady=5)

        #Standard dimentions
        width = 355
        height = 75
        
        #Buttons - Hover Buttons have custom background colour when clicked
        self.multiple_islands = FormatImage('multiple_islands.png', width=width, height=height)
        self.multipleIslands = HoverButton(master, image=self.multiple_islands, bg=bg, activebackground=bg, bd=0,
                                           command=lambda:plan_voyage(1)).grid(column=0, row=2)

        self.nearest_ports = FormatImage('nearest_ports.png', width=width, height=height)
        self.nearestPorts = HoverButton(master, image=self.nearest_ports, bg=bg, activebackground=bg, bd=0,
                                        command=lambda:plan_voyage(2)).grid(column=0, row=3, pady=10)
        #Settings Button
        self.compass = FormatImage('compass.png', width=70, height=50)
        self.settings = HoverButton(master, image=self.compass, bg=bg, fg=fg ,activebackground=bg, bd=0,
                                    command=open_settings).grid(column=0, row=0, sticky='NE', pady=10)

""" CLOSE PROGRAM """
        
def close(code=0, issue=None):
    end = True #if true, warning and end program. if false just display warning.

    if code == 0:   #error code 0: voluntary exit
        end = messagebox.askyesno('Exit?','Are you sure you want to exit?\n Your last voyage will be saved.')

    elif code == 1: #error code 1: file or path does not exist
        messagebox.showerror('Error', 'Cannot locate'+issue+'.\nYou may need to reinstall.')
        
    elif code == 2: #error code 3: file missing, restart program
        messagebox.showerror('Error', 'The Settings file was missing.\nsettings.set has been recreated.\nYou may want to revise your app customisation')
        end = False

    if end:             #check if program is supposed to end
        root.destroy()  #close parent window
        plt.close()
        sys.exit()      #end program


""" INITIALISE MAIN WINDOW """

checkFiles()

root = Tk()
main = main_window(root)
root.resizable(width=False, height=False) #don't all resize
root.geometry('375x495')
root.protocol('WM_DELETE_WINDOW', close)  #call function when close
root.mainloop()
