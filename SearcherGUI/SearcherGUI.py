#SearcherGUI.py

# A TKinter GUI developed to access a MySQL database (created with CreateDB.py) containing information about the media available on a popular streaming service.
# The GUI allows a user to filter and browse the available media, read media descriptions, and apply 'Want to See', 'Favorite', 'Watched', 'Ignore' tags to individual pieces of media.


#Author: Andrew Lopez
#startDate: April 10, 2023
#finishDate: May 18, 2023

'''
Potential Improvements:
1. Currently the database column names/sizes, and 'group' columns are hard coded into the program. Perhaps this could be refactored to be more flexible by pulling this information from the database. 
2. The functions apply_filters/apply_columns currently require many individual variables to be passed in order to fill the Filter class object. Perhaps this could be refactored to pass fewer arguments (e.g. fill a temporary Filter object during select_filters/select_columns and pass that to apply_filters/apply_columns). I'm not sure how TKinter handles this. 
3. Non-English characters are in the database but cannot be properly filtered (Symbol title filter does not include any non-English characters)
4. Non-english titles do not format properly in the table.

'''


from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import scrolledtext
import mysql.connector
from mysql.connector import errorcode


#Database Specific info 
default_columns = [
    'id', 
    'justwatch_id', 
    'title', 
    'mediatype',
    'description', 
    'release_year', 
    'age_certification', 
    'runtime', 
    'want_to_see', 
    'watched', 
    'ignored', 
    'favorite' 
]

all_columns_name = [ 
    'title', #single 30 85 max
    'justwatch_id', #single 10 
    'media_type', #single 5
    'release_year', #single 4
    'runtime', #single 7
    'age_certification', #single 8
    'media.imdb_id', #single 10
    'want_to_see', #single 1
    'watched', #single 1
    'ignored', #single 1
    'favorite', #single 1
    'imdb_info.imdb_score', #single 4 max
    'tmdb_info.tmdb_score', #single 6 max
    'tmdb_info.tmdb_popularity', #single 8 max
    'seasons.numseasons', #single 2
    'genre.genre_name',  #group 55 max 
    'country.country_name' #group 25 max 
]

all_columns_display_name = [
    'Title', #single 30 85 max
    'Justwatch ID', #single 10 
    'Type', #single 5
    'Year', #single 4
    'Runtime (min)', #single 7
    'Rating', #single 8
    'IMDB ID', #single 10
    'Want To See', #single 1
    'Watched', #single 1
    'Ignored', #single 1
    'Favorite', #single 1
    'IMDB Score', #single 4 max
    'TMDB Score', #single 6 max
    'TMDB Popularity', #single 8 max
    'Seasons', #single 2
    'Genre',  #group 55 max 
    'Country' #group 25 max
]

all_columns_size = [
    30,#'title', #single 30 85 max
    12,#'justwatch_id', #single 10 
    5,#'media_type', #single 5
    4,#'release_year', #single 4
    13,#'runtime', #single 7
    8,#'age_certification', #single 8
    10,#'media.imdb_id', #single 10
    10,#'want_to_see', #single 1
    7,#'watched', #single 1
    7,#'ignored', #single 1
    8,#'favorite', #single 1
    10,#'imdb_info.imdb_score', #single 4 max
    10,#'tmdb_info.tmdb_score', #single 6 max
    15,#'tmdb_info.tmdb_popularity', #single 8 max
    7,#'seasons.numseasons', #single 2
    55,#'genre.genre_name',  #group 55 max 
    25,#'country.country_name' #group 25 max
]

all_columns_info = {}
for index in range(len(all_columns_name)):
    all_columns_info[all_columns_name[index]] = {}
    all_columns_info[all_columns_name[index]] = {'display_name':all_columns_display_name[index],'size':all_columns_size[index]}

types = [
    'All',
    'Show',
    'Movie'
]

age_ratings = [
    'TV-Y',
    'TV-Y7',
    'TV-Y7-FV',
    'TV-G',
    'TV-PG',
    'TV-14',
    'TV-MA',
    'G',
    'PG',
    'PG-13',
    'R',
    'NC-17'
]

symbols = ["#","'","(","."]


def get_display_size():
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


def load_database(database):
    """_summary_
    Open a new window and get database login information from the user

    Arguments:
        database -- DatabaseSpecifics Class object that will store the database login information
    """
    
    loginWindow = Toplevel(root)
    loginWindow.title("MySQL Database Login")
    loginWindow.geometry("300x150")
    
    var_host = StringVar()
    var_dbname = StringVar()
    var_user = StringVar()
    var_password = StringVar()
    
    label_host = Label(loginWindow,text = "MySQL Host:")
    label_host.grid(column = 0,row = 0)
    entry_host = Entry(loginWindow,textvariable=var_host)
    entry_host.grid(column = 1, row=0)
    
    label_dbname = Label(loginWindow, text="Database Name:")
    label_dbname.grid(column = 0,row=1)
    entry_dbname = Entry(loginWindow,textvariable=var_dbname)
    entry_dbname.grid(column = 1,row=1)
    
    label_user = Label(loginWindow, text="Username:")
    label_user.grid(column=0,row=2)
    entry_user = Entry(loginWindow,textvariable=var_user)
    entry_user.grid(column=1,row=2)
    
    label_password = Label(loginWindow, text="Password:")
    label_password.grid(column=0,row=3)
    entry_password = Entry(loginWindow,textvariable=var_password)
    entry_password.grid(column=1,row=3)
    
    btn_login = Button(loginWindow,text="Login",command = lambda: get_login(database,var_host,var_dbname,var_user,var_password,loginWindow))
    btn_login.grid(column=0,row=4,columnspan=1,sticky='news')
    
    btn_cancellogin = Button(loginWindow,text="Cancel",command = lambda: loginWindow.destroy())
    btn_cancellogin.grid(column=1,row=4,columnspan=1,sticky='news')


def get_login(database,host,db,user,password,loginWindow):
    """_summary_
    move the login window information to the database class object

    Arguments:
        database -- DatabaseSpecific class object to hold the login information
        host -- TKinter Entry variable for the database Host
        db -- TKinter Entry variable for the database Name
        user -- TKinter Entry variable for the database User
        password -- TKinter Entry variable for the database Password
        loginWindow -- The TKinter window 'loginwindow'
    """    

    sqlhost = host.get()
    sqldatabase = db.get()
    sqluser = user.get()
    sqlpassword = password.get()
    
    setattr(database,'host',sqlhost)
    setattr(database,'dbname',sqldatabase)
    setattr(database,'user',sqluser)
    setattr(database,'password',sqlpassword) 
    
    loadedDB = create_connection(database) 
    
    #reset title_combo completion list because new database has been loaded
    title_combo.full_list = []
    if loadedDB:
        fill_database_class(database)
        
    finish_login(database,loginWindow)
    
    
def create_connection(database):
    """_summary_
    Use the DatabaseSpecifics class object to connect to the MySQL database entered by the user.

    Arguments:
        database -- DatabaseSpecifics Class object that will store the database connector and cursor

    Returns:
        Return bool indicating if the MySQL connection was established successfully.
    """    

    try:
        database.connector = mysql.connector.connect(host = database.host,user = database.user,password = database.password) 
    except:
        setattr(database,'connector',None)
        setattr(database,'cursor',None)
        return False
    database.cursor = database.connector.cursor()
    
    #delete password from database class object so other users can't access it
    setattr(database,'password',None)
    
    cursor = database.cursor
    cursor.execute("""USE %s""" % database.dbname) 
    return True
    
  
def fill_database_class(database):
    """_summary_
    Call other functions that will finish filling the database class object once the connection has been established.

    Arguments:
        database -- DatabaseSpecifics class object that will store the miscellaneous database information
    """    
    
    get_genre_types(database)
    get_countries(database)
    get_titles(database)
  

def get_genre_types(database):
    """_summary_
    Get the list of genre types from the database with a MySQL query and add list to database class object.

    Arguments:
        database -- DatabaseSpecifics class object that will store the genre database information and holds the database cursor.
    """    
    
    genres = []
    cursor = database.cursor
    cursor.execute("""SELECT genre_name FROM genre""")
    call = cursor.fetchall()
    for i in call:
        if i[0] == '':
            genres.append('other')
        else:
            genres.append(i[0])    
    database.genres = genres
    
    
def get_countries(database):
    """_summary_
    Get the list of countries from the database with a MySQL query and add list to database class object.

    Arguments:
        database -- DatabaseSpecifics class object that will store the country database information and holds the database cursor.
    """    
    
    countries = []
    cursor = database.cursor
    cursor.execute("""SELECT country_name FROM country""")
    call = cursor.fetchall()
    for i in call:
        if i[0] == '':
            countries.append('unknown')
        elif i[0] == 'US':
            countries.insert(0,i[0])
        else:
            countries.append(i[0])
    database.countries = countries


def get_titles(database):
    """_summary_
    Get the list of media titles from the database with a MySQL query and add list to database class object.

    Arguments:
        database -- DatabaseSpecifics class object that will store the media titles database information and holds the database cursor.
    """    
    
    cursor = database.cursor
    cursor.execute("""SELECT title FROM media""")
    string = cursor.fetchall()
    titles = []

    for i in string:
        titles.append(i[0])
    database.titles = titles


def finish_login(database,loginWindow):
    """_summary_
    Close the TKinter login window and update the login message

    Arguments:
        database -- DatabaseSpecifics class object that holds the database connector
        loginWindow -- The TKinter window 'loginwindow'
    """    
    
    loginWindow.destroy()
    update_login_message(database)
   
    
def update_login_message(database):
    """_summary_
    Check whether the database connection is available and update the login message

    Arguments:
        database -- DatabaseSpecifics class object that holds the database connector
    """    
    
    message = ''
    if database.isAvailable(): 
        message = 'Loaded database [%s] from host [%s] as user [%s]' %(database.dbname,database.host,database.user)
    else: 
        message = 'Failed to load database [%s] from host [%s] as user [%s]' %(database.dbname,database.host,database.user)
        database.reset()
    
    #update label lbl_DB to display whether a database is loaded or not
    lbl_DB.config(text=message)
    
    
def load_description_info(database,text,var_title,wanttosee_togglebtn,watched_togglebtn,ignored_togglebtn,favorite_togglebtn):
    """_summary_
    Use show_description function to get and place the media description, and set the boolean toggle buttons.

    Arguments:
        database -- DatabaseSpecifics class object that holds the database connector
        text -- tkinter textbox to hold media description
        var_title -- TKinter entry text variable that contains the media title
        wanttosee_togglebtn -- TKinter checkbox to toggle want_to_see database column
        watched_togglebtn -- TKinter checkbox to toggle watched database column
        ignored_togglebtn -- TKinter checkbox to toggle ignored database column
        favorite_togglebtn -- TKinter checkbox to toggle favorite database column
    """    

    
    show_description(database,text,var_title)

    if database.isAvailable() and var_title.get() != '':
        if get_bool_state(database,'want_to_see',var_title):
            wanttosee_togglebtn.select()
        else:
            wanttosee_togglebtn.deselect()
        
        if get_bool_state(database,'watched',var_title):
            watched_togglebtn.select()
        else:
            watched_togglebtn.deselect()
            
        if get_bool_state(database,'ignored',var_title):
            ignored_togglebtn.select()
        else:
            ignored_togglebtn.deselect()
        
        if get_bool_state(database,'favorite',var_title):
            favorite_togglebtn.select()
        else:
            favorite_togglebtn.deselect()
            
   
def toggle_bool_state(database,column,var_state,var_title):
    """_summary_
    Send a MySQL query to toggle the boolean state of the selected column.

    Arguments:
        database -- DatabaseSpecifics class object: holds the database connector
        column -- String: Name of the column to toggle
        var_state -- TKinter checkbox variable: contains the boolean column state (True/False)
        var_title -- TKinter entry text variable: contains the media title
    """    

    database.cursor.execute("""UPDATE media SET {} = %s WHERE title = %s""".format(column),(var_state.get(),var_title.get()))
    database.connector.commit()


def get_bool_state(database,column,var_title):
    """_summary_
    Send a MySQL query to get the boolean state of the selected column

    Arguments:
        database -- DatabaseSpecifics class object: holds the database connector
        column -- String: Name of the boolean column to query
        var_title -- TKinter entry text variable: contains the media title

    Returns:
        state -- Boolean: describes the column
    """    

    cursor = database.cursor
    title = var_title.get()
    if title != '':
        cursor.execute("""SELECT %s FROM media WHERE title = '%s'""" % (column,title))
        state = cursor.fetchall()[0][0]
        
    return state


def get_description(database,title):
    """_summary_

    Arguments:
        database -- DatabaseSpecifics class object: holds the database connector and cursor
        title -- string: name of media

    Returns:
        description -- string: description of the media
    """    
    

    cursor = database.cursor
    cursor.execute("""SELECT description FROM media WHERE title = '%s'""" % title) 
    description = cursor.fetchall()[0][0]

    return description


def show_description(database,text,var_title):
    """_summary_
    call get_description and insert the return string to the appropriate text field

    Arguments:
        database -- DatabaseSpecifics class object: holds the database connector and cursor
        text -- TKinter text field: where the description will be displayed
        var_title -- VarString: hold the media title
    """    
    text.config(state=NORMAL)
    text.delete('1.0',END)
    title=var_title.get()
    if title == '':
        string = 'No title specified.'
    else:
        string= get_description(database,title)
        text.insert(END, 'Title:\n'+title+'\n\nDescription:\n')

    text.insert(END, string)
    text.config(state=DISABLED)


def select_filters(filter):
    """_summary_
    Opens tkinter toplevel window to allow the user to select which filters to use.
    
    Arguments:
        filter -- MyFilter class object: holds the selected filters.
    """    
    
    
    filterWindow = Toplevel(root)
    filterWindow.title("Filters")
    filterWindow.geometry("750x600")
    orderlist = ['Ignore','Ascending','Descending']
    
    #title filters ##### WORKS
    var_titleorder = StringVar() #titles ascending/descending
    var_titleStart = StringVar()
    lbl_title = Label(filterWindow,text = 'Title:')
    lbl_title.grid(column = 0, row=0)
    startcharacters = ['All','0-9','Symbol','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    var_titleorder.set("Ignore")
    title_order = OptionMenu(filterWindow,var_titleorder,*orderlist)
    title_order.grid(column=1,row=0)
    lbl_titlestart = Label(filterWindow,text='Starts with:')
    lbl_titlestart.grid(column=2,row=0)
    var_titleStart.set("All")
    title_startswith = OptionMenu(filterWindow,var_titleStart,*startcharacters)
    title_startswith.grid(column=3,row=0)
    
    #type filter ####### WORKS
    var_type = StringVar()
    lbl_type = Label(filterWindow,text = 'Media Type')
    lbl_type.grid(column=0, row =1)
    mediatypes = ['All','Movie','Show']
    var_type.set("All")
    type_menu = OptionMenu(filterWindow,var_type,*mediatypes)
    type_menu.grid(column=1,row=1)
    
    #year filter  
    var_yearorder = StringVar()
    var_year = StringVar()
    yearoptions = ['All','Before','After','During']
    var_yearorder.set("All")
    lbl_year = Label(filterWindow,text='Release Year')
    year_menu = OptionMenu(filterWindow,var_yearorder,*yearoptions)
    year_selection = Entry(filterWindow,textvariable=var_year) 
    year_selection.insert(0, '0')
    lbl_year.grid(column = 0, row = 2)
    year_menu.grid(column = 1, row = 2)
    year_selection.grid(column = 2, row = 2)
    
    #age rating filter     ###WORKS
    selected_ratings = []
    lbl_rating = Label(filterWindow,text='Rating')
    rating_menubtn = Menubutton(filterWindow,text='Select Ratings',relief = RAISED)
    rating_menu = Menu(rating_menubtn, tearoff=0)
    lbl_rating.grid(column=0,row=3)
    var_rating_all = IntVar()
    var_rating_all.set(1) 
    rating_all = Radiobutton(filterWindow, text='All',variable=var_rating_all,value=1)
    rating_all.grid(column=1,row=3)
    rating_some = Radiobutton(filterWindow, text='Some',variable=var_rating_all,value=0)
    rating_some.grid(column=2,row=3)
    for i in age_ratings:
        selected_ratings.append(IntVar(value = 0))
        rating_menu.add_checkbutton(label = i,variable = selected_ratings[-1]) 
    rating_menubtn['menu'] = rating_menu
    rating_menubtn.grid(column=3,row=3)
    ratings = dict(zip(age_ratings,selected_ratings))
    
    #imdb score #WORKS
    var_imdbscore_inequality = StringVar()
    var_imdbscore_value = StringVar()
    var_imdbscore_order = StringVar()
    score_ordering = ['>=','<=']
    score_values = [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10'
    ]
    var_imdbscore_inequality.set(">=")
    var_imdbscore_value.set("0")
    var_imdbscore_order.set("Ignore")
    lbl_filter_imdbscore = Label(filterWindow, text = 'imdb score')
    lbl_filter_imdbscore.grid(column = 0, row = 4)
    imdbscore_order = OptionMenu(filterWindow,var_imdbscore_order,*orderlist)
    imdbscore_menu = OptionMenu(filterWindow,var_imdbscore_inequality,*score_ordering)
    imdbscore_value_menu = OptionMenu(filterWindow,var_imdbscore_value,*score_values)
    imdbscore_order.grid(column=1,row=4)
    imdbscore_menu.grid(column=2,row=4)
    imdbscore_value_menu.grid(column=3,row=4)
    
    #tmdb score ###WORKS
    var_tmdbscore_inequality = StringVar()
    var_tmdbscore_value = StringVar()
    var_tmdbscore_order = StringVar()
    var_tmdbscore_inequality.set(">=")
    var_tmdbscore_value.set("0")
    var_tmdbscore_order.set("Ignore")
    lbl_filter_tmdbscore = Label(filterWindow, text = 'tmdb score')
    lbl_filter_tmdbscore.grid(column = 0, row = 5)
    tmdbscore_order = OptionMenu(filterWindow,var_tmdbscore_order,*orderlist)
    tmdbscore_menu = OptionMenu(filterWindow,var_tmdbscore_inequality,*score_ordering)
    tmdbscore_value_menu = OptionMenu(filterWindow,var_tmdbscore_value,*score_values)
    tmdbscore_order.grid(column=1,row=5)
    tmdbscore_menu.grid(column=2,row=5)
    tmdbscore_value_menu.grid(column=3,row=5)
    
    #tmdb popularity #WORKS
    var_tmdbpop_order = StringVar()
    var_tmdbpop_order.set("Ignore")
    lbl_filter_tmdbpop = Label(filterWindow, text = 'tmdb popularity')
    lbl_filter_tmdbpop.grid(column = 0, row = 6)
    tmdbpop_menu = OptionMenu(filterWindow,var_tmdbpop_order,*orderlist)
    tmdbpop_menu.grid(column=1,row=6)
    
    #genre filter ## WORKS
    lbl_filter_genre = Label(filterWindow, text = 'genre')
    lbl_filter_genre.grid(column = 0, row = 7)
    genres_to_add = []
    genre_menubtn = Menubutton(filterWindow,text='Select Genres',relief = RAISED)
    genre_menu = Menu(genre_menubtn, tearoff=0)
    var_genre_all = IntVar()
    var_genre_all.set(1) 
    genre_all = Radiobutton(filterWindow, text='All',variable=var_genre_all,value=1)
    genre_all.grid(column=1,row=7)
    genre_some = Radiobutton(filterWindow, text='Some',variable=var_genre_all,value=0)
    genre_some.grid(column=2,row=7)
    for genre in database.genres:
        genres_to_add.append(IntVar(value = 0))
        genre_menu.add_checkbutton(label = genre,variable = genres_to_add[-1]) 
    genre_menubtn['menu'] = genre_menu
    genre_menubtn.grid(column=3,row=7)
    selected_genres = dict(zip(database.genres,genres_to_add))


    #production country filter ##WORKS
    lbl_filter_country = Label(filterWindow, text = 'country')
    lbl_filter_country.grid(column = 0, row = 8)
    
    countries_to_add = []
    country_menubtn = Menubutton(filterWindow,text='Select Countries',relief = RAISED)
    country_menu = Menu(country_menubtn, tearoff=0)
    var_country_all = IntVar()
    var_country_all.set(1)
    country_all = Radiobutton(filterWindow, text='All',variable=var_country_all,value=1)
    country_all.grid(column=1,row=8)
    country_some = Radiobutton(filterWindow, text='Some',variable=var_country_all,value=0)
    country_some.grid(column=2,row=8)
    for country in database.countries:
        countries_to_add.append(IntVar(value=0))
        country_menu.add_checkbutton(label=country,variable=countries_to_add[-1])
    country_menubtn['menu'] = country_menu
    country_menubtn.grid(column=3,row=8)
    selected_countries = dict(zip(database.countries,countries_to_add))
    #########################################################################
    

    bool_menu_options = [
        'Ignore',
        'True',
        'False'
    ]

    #want_to_see TINYINT, 
    var_wanttosee = StringVar()
    lbl_filter_wanttosee = Label(filterWindow, text = 'Want To See')
    lbl_filter_wanttosee.grid(column = 0, row = 9)
    
    var_wanttosee.set("Ignore")
    wanttosee_menu = OptionMenu(filterWindow,var_wanttosee,*bool_menu_options)
    wanttosee_menu.grid(column=1,row=9)
                
    #watched TINYINT, 
    var_watched = StringVar() 
    lbl_filter_watched = Label(filterWindow, text = 'Watched')
    lbl_filter_watched.grid(column = 0, row = 10)      
    
    var_watched.set("Ignore")
    watched_menu = OptionMenu(filterWindow,var_watched,*bool_menu_options)
    watched_menu.grid(column=1,row=10)     
                
    #ignored TINYINT, 
    var_ignored = StringVar()
    lbl_filter_ignored = Label(filterWindow, text = 'Ignored')
    lbl_filter_ignored.grid(column = 0, row = 11)            
                
    var_ignored.set("Ignore")
    ignored_menu = OptionMenu(filterWindow,var_ignored,*bool_menu_options)
    ignored_menu.grid(column=1,row=11)
                
    #favorite TINYINT
    var_favorite = StringVar()
    lbl_filter_favorite = Label(filterWindow, text = 'Favorite')
    lbl_filter_favorite.grid(column = 0, row = 12)    
    
    var_favorite.set("Ignore")
    favorite_menu = OptionMenu(filterWindow,var_favorite,*bool_menu_options)
    favorite_menu.grid(column=1,row=12)       
                
    #numEntries to show in the table filter
    var_numEntries = StringVar()
    lbl_filter_numEntries = Label(filterWindow, text = '# Entries to Display')
    lbl_filter_numEntries.grid(column = 0, row = 13)
    
    numEntries_entry = Entry(filterWindow,textvariable=var_numEntries) 
    numEntries_entry.insert(0, '100')
    numEntries_entry.grid(column=1,row=13)
    
    #error message (to test)
    lbl_error_message = Label(filterWindow,text = '')
    lbl_error_message.grid(column=0,row=15,columnspan=4,sticky=W)
    
    #button to apply filters to table
    btn_applyfilters = Button(filterWindow,text="Apply",command=lambda: apply_filters(filter,filterWindow,var_titleorder,var_titleStart,var_type,var_yearorder,var_year,var_numEntries,var_rating_all,ratings,var_imdbscore_inequality,var_imdbscore_order,var_imdbscore_value,var_tmdbscore_inequality,var_tmdbscore_order,var_tmdbscore_value,var_tmdbpop_order,var_genre_all,selected_genres,var_country_all,selected_countries,var_wanttosee,var_watched,var_ignored,var_favorite,lbl_error_message))
    btn_applyfilters.grid(column=0,row=16)
    btn_cancelfilters = Button(filterWindow,text="Cancel",command=lambda: filterWindow.destroy() )
    btn_cancelfilters.grid(column=1,row=16)
    
    
def apply_filters(filter,filterWindow,titleorder,titlestart,typefilter,year_order,year,numEntries,rating_all,selected_ratings,imdbscore_inequality,imdbscore_order,imdbscore,tmdbscore_inequality,tmdbscore_order,tmdbscore,tmdbpopularity_order,genre_all,selected_genres,country_all,selected_countries,wanttosee,watched,ignored,favorite,lbl_error_message): 
    """_summary_
    Get the user selected filters from select_filters function and insert the values into the myfilter class object.

    Arguments:
        filter -- MyFilter class object: holds the selected filters.
        filterWindow -- TKinter toplevel window: window that holds the filter fields for the user to enter.
        titleorder -- StringVar: holds whether the title will be Ignored, ordered Ascending or ordered Descending
        titlestart -- StringVar: holds the starting letter of the title to filter
        typefilter -- StringVar: holds whether the media should be filtered by type
        year_order -- StringVar: holds how the media release year should be filtered
        year -- StringVar: holds the year of media release to be used as a reference for filtering
        numEntries -- StringVar: holds the number of entries to be displayed in the database information table
        rating_all -- IntVar: holds whether the media should be filtered by age rating
        selected_ratings -- dictionary: holds string:boolean IntVar pairs which describe each age rating and whether it should be allowed/disallowed
        imdbscore_inequality -- StringVar: holds the selected inequality that will be used to apply the imdb score filter
        imdbscore_order -- StringVar: holds how the imdb score should be filtered
        imdbscore -- StringVar: holds the numerical value to be used as a reference for filtering imdb score
        tmdbscore_inequality -- StringVar: holds the selected inequality that will be used to apply the tmdb score filter
        tmdbscore_order -- StringVar: holds how the tmdb score should be filtered
        tmdbscore -- StringVar: holds the numerical value to be used as a reference for filtering tmdb score
        tmdbpopularity_order -- StringVar: holds how the tmdb popularity should be filtered
        genre_all -- IntVar: holds whether to filter media genre
        selected_genres -- dictionary: holds string:boolean IntVar pairs which describe each genre and whether it should be allowed/disallowed
        country_all -- IntVar: holds whether to filter media production company
        selected_countries -- dictionary: holds string:boolean IntVar pairs which describe each production country and whether it should be allowed/disallowed
        wanttosee -- StringVar: holds whether the want_to_see column should be filtered or ignored
        watched -- StringVar: holds whether the watched column should be filtered or ignored
        ignored -- StringVar: holds whether the ignored column should be filtered or ignored
        favorite -- StringVar: holds whether the favorite column should be filtered or ignored
        lbl_error_message -- TKinter label: used to display error messages when a user selected filter variable is prohibited
    """    

    # title filter
    if titleorder.get() == 'Ignore':
        filter.title_order = "IGNORE"
    if titleorder.get() == 'Ascending':
        filter.title_order = 'ASC'
    elif titleorder.get() == 'Descending':
        filter.title_order = 'DESC'
    if titlestart.get() == 'All':
        filter.title_startswith = ''
    else:
        filter.title_startswith = titlestart.get()
    
    # media type filter 
    filter.media_type = typefilter.get().upper()
    
    # age rating filter
    filter.selected_ratings = []
    filter.ratings_all = rating_all.get()
    for i in selected_ratings:
        if selected_ratings[i].get():
            filter.selected_ratings.append(i)
        
    # imdb score filter 
    if imdbscore_order.get() == 'Ignore':
        filter.imdb_score_order = 'IGNORE'
    elif imdbscore_order.get() == 'Ascending':
        filter.imdb_score_order = 'ASC'
    elif imdbscore_order.get() == 'Descending':
        filter.imdb_score_order = 'DESC'
    filter.imdb_score_inequality = imdbscore_inequality.get()
    filter.imdb_score = int(imdbscore.get())
    
    # tmdb score filter
    if tmdbscore_order.get() == 'Ignore':
        filter.tmdb_score_order = 'IGNORE'
    elif tmdbscore_order.get() == 'Ascending':
        filter.tmdb_score_order = 'ASC'
    elif tmdbscore_order.get() == 'Descending':
        filter.tmdb_score_order = 'DESC'
    filter.tmdb_score_inequality = tmdbscore_inequality.get()
    filter.tmdb_score = int(tmdbscore.get())
    
    # tmdb popularity filter 
    if tmdbpopularity_order.get() == 'Ignore':
        filter.tmdb_popularity_order = 'IGNORE'
    elif tmdbpopularity_order.get() == 'Ascending':
        filter.tmdb_popularity_order = 'ASC'
    elif tmdbpopularity_order.get() == 'Descending':
        filter.tmdb_popularity_order = 'DESC'
    
    # genre filter
    filter.selected_genres = []
    filter.genres_all = genre_all.get()
    for genre in selected_genres:
        if selected_genres[genre].get():
            filter.selected_genres.append(genre)
    
    # country filter
    filter.selected_countries = []
    filter.countries_all = country_all.get()
    for country in selected_countries:
        if selected_countries[country].get():
            filter.selected_countries.append(country)
    
    # want to see filter
    if wanttosee.get() == 'Ignore':
        filter.wanttosee = 'IGNORE'
    elif wanttosee.get() == 'True':
        filter.wanttosee = '1'
    elif wanttosee.get() == 'False':
        filter.wanttosee = '0'
    
    # watched filter
    if watched.get() == 'Ignore':
        filter.watched = 'IGNORE'
    elif watched.get() == 'True':
        filter.watched = '1'
    elif watched.get() == 'False':
        filter.watched = '0'
    
    # ignored filter
    if ignored.get() == 'Ignore':
        filter.ignored = 'IGNORE'
    elif ignored.get() == 'True':
        filter.ignored = '1'
    elif ignored.get() == 'False':
        filter.ignored = '0'
        
    # favorite filter
    if favorite.get() == 'Ignore':
        filter.favorite = 'IGNORE'
    elif favorite.get() == 'True':
        filter.favorite = '1'
    elif favorite.get() == 'False':
        filter.favorite = '0'
    
    
    # check for errors in year and numEntries entries
    year_error = False
    error_string = ''
    try:
        int(year.get())
    except:
        year_error = True
    if not year_error:
        if int(year.get()) < 0:
            year_error = True
    if year_error:
        error_string = 'Release Year: Must be positive integer. '
        
    entries_error = False
    try:
        int(numEntries.get())
    except:
        entries_error = True
    if not entries_error:
        if int(numEntries.get()) < 0:
            entries_error = True
    if entries_error:
        error_string += 'Number of Entries: Must be positive integer.'
        
    if error_string != '':
        lbl_error_message.config(text=error_string)
    
    # add year and numEntries to filter class after error checking
    # year filter
    if year_order.get() == 'All':
        filter.year_order = 'IGNORE'
    elif year_order.get() == 'Before':
        filter.year_order = '<'
    elif year_order.get() == 'After':
        filter.year_order = '>'
    elif year_order.get() == 'During':
        filter.year_order = '='
    filter.year = year.get()
    
    # numEntries filter
    filter.numEntries = numEntries.get()
    
  
        

    
    # destroy window
    filterWindow.destroy()
    

class DatabaseSpecifics: 
    """
    A class used to hold database specific information, particularly parameters necessary for connection.
    
    Parameters:
            host -- String: name of MySQL database host
            dbname -- String: name of MySQL database
            user -- String: name of MySQL database user
            password -- String: name of MySQL database password
            connector -- mysql.connector:
            cursor -- mysql.connector.cursor:
            titles -- list: list of media titles found in the database
            genres -- list: list of genres found in the database
            countries -- list: list of production country codes found in the database
            
    """    
    
    # constructor
    def __init__(self):
        """
        Parameters:
            host -- String: name of MySQL database host
            dbname -- String: name of MySQL database
            user -- String: name of MySQL database user
            password -- String: name of MySQL database password
            connector -- mysql.connector:
            cursor -- mysql.connector.cursor:
            titles -- list: list of media titles found in the database
            genres -- list: list of genres found in the database
            countries -- list: list of production country codes found in the database
        """       
         
        self.host = None
        self.dbname = None
        self.user = None
        self.password = None
        self.connector = None
        self.cursor = None
        self.titles = []
        self.genres = []
        self.countries = []

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value:str):
        self._host = value
        
    @property
    def dbname(self):
        return self._dbname

    @dbname.setter
    def dbname(self, value:str):
        self._dbname = value
        
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value:str):
        self._user = value

    def isAvailable(self):
        """_summary_
        Check if the mysql.connector and mysql.connector.cursor have sucessfully been created.

        Returns:
            Boolean
        """        
        if self.connector != None and self.cursor != None:
            return True
        else:
            return False
    
    def reset(self):
        """_summary_: Reset object when a connection fails to establish"""        
        self.host = None
        self.dbname = None
        self.user = None
        self.password = None
        self.connector = None
        self.cursor = None
        self.titles = []
        self.genres = []
        self.countries = []


class MyFilter: 
    """_summary_
    A class to hold user selected filter information to apply to the database
    
    Parameters:
        numEntries -- Int: determines number of media titles to display to the user.
        title_order -- String: determines how to order media titles column from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","ASC","DESC"] 
        single_columns -- List: Contains user selected columns to display. Only columns that ARE NOT part of an association table are included. DEFAULT = ['title','media_type']
        group_columns -- List: Contains user selected columns to display. Only columns that ARE part of an association table are included. DEFAULT = ['genre.genre_name']. MYSQL "GROUP BY" command is required when these are requested.
        title_startswith -- String: determines which titles to filter by starting character. DEFAULT = '' (No filter applied).
        media_type -- String: determines how to filter media_type column from the database. DEFAULT = 'ALL' (No filter applied). OPTIONS = ["ALL","SHOW","MOVIE"]
        ratings_all -- Boolean: Determines whether to apply a filter to age_certification column values from the database. DEFAULT = 1 (No filter applied). Used in conjunction with selected_ratings.
        selected_ratings -- List[String]: Contains name of age_certification column values which are allowed. DEFAULT = []. Used in conjunction with ratings_all.
        imdb_score_order -- String: determines how to order imdb score column from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","ASC","DESC"]. Used in conjunction with imdb_score_inequality and imdb_score.
        imdb_score_inequality -- String: Determines how to filter media by imdb_score column value. DEFAULT = '>='. OPTIONS = ['>=','<=']. Used in conjunction with imdb_score_order and imdb_score.
        imdb_score -- String: determines how to filter the imdb_score column value. DEFAULT = 0. Used in conjunction with imdb_score_order and imdb_score_inequality.
        tmdb_score_order -- String: determines how to order tmdb score column from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","ASC","DESC"]. Used in conjunction with tmdb_score_inequality and tmdb_score.
        tmdb_score_inequality -- String: Determines how to filter media by tmdb_score column value. DEFAULT = '>='. OPTIONS = ['>=','<=']. Used in conjunction with tmdb_score_order and tmdb_score.
        tmdb_score -- String: determines how to filter the imdb_score column value. DEFAULT = 0. Used in conjunction with tmdb_score_order and tmdb_score_inequality.
        tmdb_popularity_order -- String: determines how to order tmdb popularity column from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","ASC","DESC"]
        year_order -- String: determines how to order release_year column from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","ASC","DESC"]. Used in conjunction with year.
        year -- String: determines how to filter the release_year column value. DEFAULT = 0. Used in conjunction with year_order.
        genres_all -- Boolean: Determines whether to apply a filter to genre column values from the database. DEFAULT = 1 (No filter applied). Used in conjunction with selected_genres.
        selected_genres -- List[String]: Contains name of genre_name column values which are allowed. DEFAULT = []. Used in conjunction with genres_all.
        countries_all -- Boolean: Determines whether to apply a filter to country_name column values from the database. DEFAULT = 1 (No filter applied). Used in conjunction with selected_countries.
        selected_countries -- List[String]: Contains name of country_name column values which are allowed. DEFAULT = []. Used in conjunction with countries_all.
        wanttosee -- String: determines how to filter want_to_see column value from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","TRUE","FALSE"]
        watched -- String: determines how to filter watched column value from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","TRUE","FALSE"]
        ignored -- String: determines how to filter ignored column value from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","TRUE","FALSE"]
        favorite -- String: determines how to filter favorite column value from the database. DEFAULT = "IGNORE". OPTIONS = ["IGNORE","TRUE","FALSE"]
    """    
    
    def __init__(self, numEntries):
        """
        Parameters:
            numEntries -- number of entries to display to the user.
        """
        
        self.numEntries = numEntries
        self.title_order = "IGNORE" 
        self.single_columns = ['title','media_type'] # Columns that are not part of an association table
        self.group_columns = ['genre.genre_name'] # Columns that are part of an association table. MYSQL "GROUP BY" command is required when these are requested.
        self.title_startswith = ''
        self.media_type = 'ALL'
        self.ratings_all = True
        self.selected_ratings = []
        self.imdb_score_order = 'IGNORE'
        self.imdb_score_inequality = '>='
        self.imdb_score = 0
        self.tmdb_score_order = 'IGNORE'
        self.tmdb_score_inequality = '>='
        self.tmdb_score = 0
        self.tmdb_popularity_order = 'IGNORE'
        self.year_order = "IGNORE"
        self.year = 0
        self.genres_all = True
        self.selected_genres = []
        self.countries_all = True
        self.selected_countries = []
        self.wanttosee = 'IGNORE'
        self.watched = 'IGNORE'
        self.ignored = 'IGNORE'
        self.favorite = 'IGNORE'
        
    @property
    def numEntries(self):
        return self._numEntries
    
    @numEntries.setter
    def numEntries(self, v:int): 
        """_summary_
        Update the number of entries to display to the user.

        Arguments:
            v -- Int: new number of entries value

        Raises:
            TypeError: new value is not an integer
            Exception: new value is less than zero
        """        
        
        try:
            int(v)
        except:
            raise TypeError('# Entries to Display: Only integers are allowed')
        if not (int(v) > 0): raise Exception("numEntries must be greater than zero")
        self._numEntries = v
        
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, v:int): 
        """_summary_
        Update the release year filter value. Must be an integer representing the year.

        Arguments:
            v -- new release year value

        Raises:
            TypeError: new value is not an integer
            Exception: new value is less than zero
        """        
        
        try:
            int(v)
        except:
            raise TypeError('Release Year: Only integers are allowed')
        if not (int(v) >= 0): raise Exception("Year must be positive")
        self._year = v

        
class AutocompleteCombobox(ttk.Combobox):
        '''
        Class from tkentrycomplete.py

        A Tkinter widget that features autocompletion.

        Created by Mitja Martini on 2008-11-29.
        Updated by Russell Adams, 2011/01/24 to support Python 3 and Combobox.
        Updated by Dominic Kexel to use Tkinter and ttk instead of tkinter and tkinter.ttk
        Updated by Andrew Lopez to shrink and expand the completion list depending on the comparison with the widget value.
        '''

        
        full_list = [] 

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                if self.full_list == []:
                    self.full_list = sorted(completion_list, key=str.lower) 
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu
  
        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        #self.delete(0,tkinter.END) # turned off entry autocompletion as it interfered with backspaces
                        #self.insert(0,self._hits[self._hit_index]) # turned off entry autocompletion as it interfered with backspaces
                        self.select_range(self.position,END) 
                        self.set_completion_list(_hits) 

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(INSERT), END)
                        self.position = self.index(END)
                if event.keysym == "Left":
                        if self.position < self.index(END): # delete the selection
                                self.delete(self.position, END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, END)
                if event.keysym == "Right":
                        self.position = self.index(END) # go to end (no selection)
                
                if len(event.keysym) == 1 or event.keysym == 'BackSpace' or event.keysym == 'Left':
                        self.set_completion_list(self.full_list)
                        self.autocomplete()


def select_columns(filter):
    """_summary_
    Opens a tkinter toplevel window and allows the user to select which columns to display.

    Arguments:
        filter -- MyFilter class object: holds the selected columns.
    """   
    
    columnWindow = Toplevel(root)
    columnWindow.title("Columns")
    columnWindow.geometry("550x600")
    
    
    lbl_selectcol = Label(columnWindow,text="Select Columns To Display")
    lbl_selectcol.grid(column=0,row=0)
    
    # columns 
    var_allcolumns = IntVar()
    chkbtn_col_all = Checkbutton(columnWindow,text = "Show All Columns",variable=var_allcolumns,onvalue=1,offvalue=0,height=1,width=16,padx=15,anchor=W)
    chkbtn_col_all.grid(column=0,row=1,sticky='W')
    # justwatch_id 
    var_justwatch_id = IntVar()
    chkbtn_col_justwatchid = Checkbutton(columnWindow,text = "JustwatchID",variable=var_justwatch_id,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_justwatchid.grid(column=0,row=2,sticky='W')
    # media_type
    var_type = IntVar()
    chkbtn_col_type = Checkbutton(columnWindow,text = "Media Type",variable=var_type,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_type.grid(column=0,row=3,sticky='W')
    # release_year
    var_year = IntVar()
    chkbtn_col_year = Checkbutton(columnWindow,text = "Release Year",variable=var_year,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_year.grid(column=0,row=4,sticky='W')
    # runtime
    var_runtime = IntVar()
    chkbtn_col_runtime = Checkbutton(columnWindow,text = "Runtime",variable=var_runtime,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_runtime.grid(column=0,row=5,sticky='W')
    # age_certification
    var_rating = IntVar()
    chkbtn_col_rating = Checkbutton(columnWindow,text = "Rating",variable=var_rating,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_rating.grid(column=0,row=6,sticky='W')
    # imdb_id
    var_imdbid = IntVar()
    chkbtn_col_imdbid = Checkbutton(columnWindow,text = "IMDB ID",variable=var_imdbid,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_imdbid.grid(column=0,row=7,sticky='W')
    # want_to_see
    var_wanttosee = IntVar()
    chkbtn_col_wanttosee = Checkbutton(columnWindow,text = "Want To See",variable=var_wanttosee,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_wanttosee.grid(column=0,row=8,sticky='W')
    # watched
    var_watched = IntVar()
    chkbtn_col_watched = Checkbutton(columnWindow,text = "Watched",variable=var_watched,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_watched.grid(column=0,row=9,sticky='W')
    # ignored
    var_ignored = IntVar()
    chkbtn_col_ignored = Checkbutton(columnWindow,text = "Ignored",variable=var_ignored,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_ignored.grid(column=0,row=10,sticky='W')
    # favorite
    var_favorite = IntVar()
    chkbtn_col_favorite = Checkbutton(columnWindow,text = "Favorite",variable=var_favorite,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_favorite.grid(column=0,row=11,sticky='W')
    # imdb_info columns    (imdb_score,imdb_votes)
    var_imdbscore = IntVar()
    chkbtn_col_imdbscore = Checkbutton(columnWindow,text = "IMDB Score",variable=var_imdbscore,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_imdbscore.grid(column=0,row=12,sticky='W')
    # tmdb_info table columns (tmdb_score,tmdb_popularity)
    var_tmdbscore = IntVar()
    chkbtn_col_tmdbscore = Checkbutton(columnWindow,text = "TMDB Score",variable=var_tmdbscore,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_tmdbscore.grid(column=0,row=13,sticky='W')
    var_tmdbpop = IntVar()
    chkbtn_col_tmdbpop = Checkbutton(columnWindow,text = "TMDB Popularity",variable=var_tmdbpop,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_tmdbpop.grid(column=0,row=14,sticky='W')
    # genre table column (genre_name)
    var_genre = IntVar()
    chkbtn_col_genre = Checkbutton(columnWindow,text = "Genres",variable=var_genre,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_genre.grid(column=0,row=15,sticky='W')
    # seasons table column (numseasons)
    var_seasons = IntVar()
    chkbtn_col_seasons = Checkbutton(columnWindow,text = "Seasons",variable=var_seasons,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_seasons.grid(column=0,row=16,sticky='W')
    # country table column (country_name)
    var_country = IntVar()
    chkbtn_col_country = Checkbutton(columnWindow,text = "Country",variable=var_country,onvalue=1,offvalue=0,height=1,width=13,padx=15,anchor=W)
    chkbtn_col_country.grid(column=0,row=17,sticky='W')
    
    # button to apply filters to table
    btn_applycolumns = Button(columnWindow,text="Apply",command=lambda: apply_columns(filter,columnWindow,var_allcolumns,var_justwatch_id,var_type,var_year,var_runtime,var_rating,var_imdbid,var_wanttosee,var_watched,var_ignored,var_favorite,var_imdbscore,var_tmdbscore,var_tmdbpop,var_genre,var_seasons,var_country) )
    btn_applycolumns.grid(column=0,row=18)
    
    btn_cancelcolumns = Button(columnWindow,text="Cancel",command=lambda: columnWindow.destroy() )
    btn_cancelcolumns.grid(column=1,row=18)


def apply_columns(filter,columnWindow,allcolumns,justwatch_id,type,year,runtime,rating,imdbid,wanttosee,watched,ignored,favorite,imdbscore,tmdbscore,tmdbpop,genre,seasons,country):
    """_summary_
    Get the user selected filters from select_filters function and insert the values into the filter class object.

    Arguments:
        filter -- _description_
        columnWindow -- tkinter toplevel window: where the user selects which columns to display
        allcolumns -- IntVar: holds whether to display all columns
        justwatch_id -- IntVar: holds whether to display the justwatch_id column
        type -- IntVar: holds whether to display the media_type column
        year -- IntVar: holds whether to display the release_year column
        runtime -- IntVar: holds whether to display the runtime column
        rating -- IntVar: holds whether to display the age_certification column
        imdbid -- IntVar: holds whether to display the imdb_id column
        wanttosee -- IntVar: holds whether to display the want_to_see column
        watched -- IntVar: holds whether to display the watched column
        ignored -- IntVar: holds whether to display the ignored column
        favorite -- IntVar: holds whether to display the favorite column
        imdbscore -- IntVar: holds whether to display the imdb_score column
        tmdbscore -- IntVar: holds whether to display the tmdb_score column
        tmdbpop -- IntVar: holds whether to display the tmdb_popularity column
        genre -- IntVar: holds whether to display the genre_name column
        seasons -- IntVar: holds whether to display the seasons column
        country -- IntVar: holds whether to display the country_name column
    """    
    
    #columns as list
    single_columns = ['title']
    group_columns = []
    if justwatch_id.get() or allcolumns.get(): #WORKS
        single_columns.append('justwatch_id')
    if type.get() or allcolumns.get(): #WORKS
        single_columns.append('media_type')
    if year.get() or allcolumns.get(): #WORKS
        single_columns.append('release_year')    
    if runtime.get() or allcolumns.get(): #WORKS
        single_columns.append('runtime')
    if rating.get() or allcolumns.get(): #WORKS
        single_columns.append('age_certification')
    if imdbid.get() or allcolumns.get(): #WORKS
        single_columns.append('media.imdb_id')
    if wanttosee.get() or allcolumns.get(): #WORKS
        single_columns.append('want_to_see')
    if watched.get() or allcolumns.get(): #WORKS
        single_columns.append('watched')
    if ignored.get() or allcolumns.get(): #WORKS
        single_columns.append('ignored')   
    if favorite.get() or allcolumns.get(): #WORKS
        single_columns.append('favorite')  
    if imdbscore.get() or allcolumns.get(): #WORKS
        single_columns.append('imdb_info.imdb_score')  
    
    #tmdb columns
    if tmdbscore.get() or allcolumns.get(): #WORKS
        single_columns.append('tmdb_info.tmdb_score')  
    if tmdbpop.get() or allcolumns.get(): #WORKS
        single_columns.append('tmdb_info.tmdb_popularity')  
    
    #seasons column #WORKS
    if seasons.get() or allcolumns.get(): 
        single_columns.append('seasons.numseasons')
    
    #genre column
    if genre.get() or allcolumns.get(): #WORKS
        group_columns.append('genre.genre_name')
        
    #country column #WORKS
    if country.get() or allcolumns.get(): 
        group_columns.append('country.country_name')
    
    
    
    setattr(filter,'single_columns',single_columns)
    setattr(filter,'group_columns',group_columns)
    
    columnWindow.destroy()


def fill_columnstext(text,filter):
    """_summary_
    Get the user selected columns, format them into a string, and insert them into the tkinter text field for column names

    Arguments:
        text -- tkinter text field: holds the user selected column names.
        filter -- MyFilter class object: holds the selected columns.
    """    
    
    text.config(state=NORMAL)
    text.delete('1.0',END)
    string = ''
    for column in filter.single_columns:
        stringpart = all_columns_info[column]['display_name']
        stringpart = stringpart.center(all_columns_info[column]['size'])+ ' | '
        string += stringpart
    for column in filter.group_columns:
        stringpart = all_columns_info[column]['display_name']
        stringpart = stringpart.center(all_columns_info[column]['size'])+ ' | '
        string += stringpart
    
    text.insert(END, string)
    text.config(state=DISABLED)


def get_mysql_select_string(filter):
    """_summary_
    Accesses the columns selected by the user (saved in the myfilter class object) and produces a string containing the appropriate "SELECT FROM" MySQL query 

    Arguments:
        filter -- MyFilter class object: holds the selected columns and filter variables.

    Returns:
        select_string -- String: contains the "SELECT [] FROM []" portion of the MySQL Query
    """    
       
    select_string = ''
    single_columns = ''
    group_columns = ''

    single_columns = ','.join(filter.single_columns)
    if filter.group_columns != []:
        for column in filter.group_columns:
            group_columns = group_columns+",GROUP_CONCAT(DISTINCT %s SEPARATOR ', ')"%column

    select_string = "SELECT "+single_columns+group_columns+' FROM media'  
    return select_string


def get_mysql_join_string(filter):
    """_summary_
    Accesses the columns and filters selected by the user (saved in the myfilter class object) and produces a string containing the appropriate MYSQL "JOIN" queries. 

    Arguments:
        filter -- MyFilter class object: holds the selected columns and filter variables.

    Returns:
        join_string -- String: contains the "SELECT [] FROM []" portion of the MySQL Query
    """    
    

    join_string = ''

    ##imdb score is requested   ##WORKS
    if any("imdb_info" in column for column in filter.single_columns) or filter.imdb_score_order != "IGNORE" or filter.imdb_score != 0 or filter.imdb_score_inequality == "<=": 
        join_string += " INNER JOIN imdb_info ON media.imdb_id=imdb_info.imdb_id"
    
    #### tmdb score/popularity is requested ###WORKS
    if any("tmdb_info" in column for column in filter.single_columns) or filter.tmdb_score_order != "IGNORE" or filter.tmdb_score != 0 or filter.tmdb_score_inequality == "<=" or filter.tmdb_popularity_order != "IGNORE": 
        join_string += " INNER JOIN tmdb_info ON media.id=tmdb_info.media_id"

    #genre is requested #WORKS
    if any("genre." in column for column in filter.group_columns) or not filter.genres_all and len(filter.selected_genres) != 0:
        join_string += " INNER JOIN media_genre ON media.id=media_genre.media_id INNER JOIN genre ON genre.id=media_genre.genre_id" #WORKS
    
    #seasons is requested #WORKS
    if any("seasons." in column for column in filter.single_columns):
        join_string += " LEFT JOIN seasons ON media.id=seasons.media_id" 
    
    #country is requested #WORKS
    if any("country." in column for column in filter.group_columns) or not filter.countries_all and len(filter.selected_countries) != 0: #WORKS
        join_string += " INNER JOIN media_country ON media.id=media_country.media_id INNER JOIN country ON country.id=media_country.country_id" 
    
    return join_string


def get_mysql_where_string(filter):
    """_summary_
    Accesses the filters selected by the user (saved in the myfilter class object) and produces a string containing the appropriate MYSQL "WHERE" queries. 

    Arguments:
        filter -- MyFilter class object: holds the selected columns and filter variables.

    Returns:
        where_string -- String: contains the "SELECT [] FROM []" portion of the MySQL Query
    """    
    
    where_string = ''
    
    
    # Title filters
    title_counter = 0
    if filter.title_startswith != '':
        where_string += ' WHERE'
        if filter.title_startswith == '0-9':
            for i in range(9):
                if title_counter != 0:
                    where_string += ' OR'
                where_string += " title LIKE '%s%%'" %i
                title_counter += 1
        elif filter.title_startswith == 'Symbol':
            for i in range(len(symbols)):
                if title_counter != 0:
                    where_string += ' OR'
                where_string += " title LIKE '\%s%%'" %symbols[i]
                title_counter += 1
        else:
            where_string += " title LIKE '%s%%'" %filter.title_startswith

    # type filter
    if filter.media_type != 'ALL':
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else:
            where_string += ' AND'
        where_string += " media_type = '%s'" %filter.media_type
        
    # age certification filter
    ratings_counter = 0
    if not filter.ratings_all and len(filter.selected_ratings) != 0:
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        for rating in filter.selected_ratings:
            if ratings_counter != 0:
                where_string += ' OR'
            where_string += " age_certification = '%s'" %rating
            ratings_counter += 1
    
    # imdb score filter
    if filter.imdb_score_inequality == "<=" or filter.imdb_score != 0:
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        where_string += ' imdb_score ' + filter.imdb_score_inequality + str(filter.imdb_score)

    # tmdb score filter 
    if filter.tmdb_score_inequality == "<=" or filter.tmdb_score != 0: 
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        where_string += ' tmdb_score ' + filter.tmdb_score_inequality + str(filter.tmdb_score)

    # wanttosee filter
    if filter.wanttosee != 'IGNORE': 
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        where_string += " want_to_see = %s" %filter.wanttosee
        
    # watched filter
    if filter.watched != 'IGNORE':
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        where_string += " watched = %s" %filter.watched
    
    # ignored filter
    if filter.ignored != 'IGNORE':
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        where_string += " ignored = %s" %filter.ignored
    
    # favorite filter
    if filter.favorite != 'IGNORE':
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        where_string += " favorite = %s" %filter.favorite
    
    # release year filter 
    if filter.year_order != 'IGNORE':
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        where_string += " release_year %s %s" %(filter.year_order,filter.year)
    
    # genre filter
    genres_counter = 0
    if not filter.genres_all and len(filter.selected_genres) != 0:
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        for genre in filter.selected_genres:
            if genre == 'other':
                genre_name = ''
            else:
                genre_name = genre
            if genres_counter != 0:
                where_string += ' OR'
            where_string += " media.id IN (SELECT media_id FROM media_genre WHERE genre_id = (SELECT id FROM genre WHERE genre_name = '%s') )" %genre_name
            genres_counter += 1
        
    # country filter 
    countries_counter = 0
    if not filter.countries_all and len(filter.selected_countries) != 0:
        if where_string.find("WHERE") == -1:
            where_string += ' WHERE'
        else: 
            where_string += " AND" 
        for country in filter.selected_countries:
            if country == 'other':
                country_name = ''
            else:
                country_name = country
            if countries_counter != 0:
                where_string += ' OR'
            where_string += " media.id IN (SELECT media_id FROM media_country WHERE country_id = (SELECT id FROM country WHERE country_name = '%s') )" %country_name
            countries_counter += 1

    return where_string


def get_mysql_order_string(filter):
    """_summary_
    Accesses the filters selected by the user (saved in the myfilter class object) and produces a string containing the appropriate MYSQL "ORDER BY" query. 

    Arguments:
        filter -- MyFilter class object: holds the selected columns and filter variables.

    Returns:
        order_string -- String: contains the "SELECT [] FROM []" portion of the MySQL Query
    """    
    
    order_string = ''
    order_counter = 0
    
    # check that at least one order filter is selected
    if filter.title_order != 'IGNORE' or filter.imdb_score_order != 'IGNORE' or filter.tmdb_score_order != 'IGNORE' or filter.tmdb_popularity_order != 'IGNORE':
        order_string += ' ORDER BY '
    else:
        return order_string    
        
    # title filter
    if filter.title_order != "IGNORE":
        order_string += 'title %s' % filter.title_order
        order_counter += 1
    
    # imdb score filter
    if filter.imdb_score_order != "IGNORE":
        if order_counter > 0:
            order_string += ', '
        order_string += "imdb_score %s" %filter.imdb_score_order
        order_counter += 1
    
    # tmdb score filter
    if filter.tmdb_score_order != "IGNORE":
        if order_counter > 0:
            order_string += ', '
        order_string += "tmdb_score %s" %filter.tmdb_score_order
        order_counter += 1
    
    # tmdb_popularity filter 
    if filter.tmdb_popularity_order != "IGNORE":
        if order_counter > 0:
            order_string += ', '
        order_string += "tmdb_popularity %s" %filter.tmdb_popularity_order
        order_counter += 1
        

    return order_string
 
    
def get_mysql_group_string(filter,order_string,join_string):
    """_summary_
    Accesses the columns and filters selected by the user (through the myfilter class object, the order_string, and the join_string) and produces a string containing the appropriate MYSQL "GROUP BY" query. 

    Arguments:
        filter -- MyFilter class object: holds the selected columns and filter variables.
        order_string -- String: output of get_mysql_order_string
        join_string -- String: output of get_mysql_join_string

    Returns:
        group_string -- String: contains the appropriate MYSQL "GROUP BY" query.
    """    
    
    group_string = ''
    single_columns = ','.join(filter.single_columns)

    # get list of columns called by the order_string (from get_mysql_order_string)
    order_columns = order_string.replace('ORDER BY','').replace('ASC','').replace('DESC','').replace(',','').strip().split()
    for column in order_columns:
        if single_columns.find(column) == -1:
            single_columns += ','+column        #add columns requested by user filters to list even if they will not be displayed in the table 
    
    # add GROUP BY command if genre/country information is requested (checking filter.single_columns, filter.group_columns, order_string, join_string) 
    if join_string.find('genre') != -1 or join_string.find('country') != -1:
        group_string = " GROUP BY %s" % (single_columns)
    
    return group_string


def get_dbinfo(database,filter):
    """_summary_
    Use myFilter class object build and execute appropriate MYSQL query then return formatted string to display in media information table

    Arguments:
        database -- DatabaseSpecifics class object: holds the database information, connector, and cursor
        filter -- MyFilter class object: holds the selected columns and filter variables.

    Returns:
        media_table_string -- String: contained formatted database information to display to the user.
    """    
    
    
    select_string = ''
    where_string = ''
    join_string = ''
    group_string = ''
    order_string = ''
    
    select_string = get_mysql_select_string(filter)
    join_string = get_mysql_join_string(filter)
    where_string = get_mysql_where_string(filter)
    order_string = get_mysql_order_string(filter)
    group_string = get_mysql_group_string(filter,order_string,join_string)
    
    ###### EXECUTE SQL STATEMENT #####
    command_string = select_string+join_string+where_string+group_string+order_string
    cursor = database.cursor
    cursor.execute(command_string) #works
    media_info = cursor.fetchall()[:int(filter.numEntries)] # a list of tuples containing media information from mysql database


    selected_columns = filter.single_columns + filter.group_columns
    media_table_string = ''
    for media in media_info:
        for index in range(len(media)):
            columndata = media[index]
            size_limit = all_columns_info[selected_columns[index]]['size']
            media_table_string += str(columndata)[:size_limit].center(size_limit) + ' | '
        media_table_string += '\n'

            
    return media_table_string


def update_table(database,txt_table,txt_columns,filter):
    """_summary_
    Apply the myfilter class object variables to query the database and update the appropriate tkinter text fields

    Arguments:
        database -- DatabaseSpecifics class object: holds the database information, connector, and cursor
        txt_table -- tkinter text field: will display the information received from the database.
        txt_columns -- tkinter text field: will display the names of the columns selected by the user.
        filter -- MyFilter class object: holds the selected columns and filter variables.
    """    
    
    fill_columnstext(txt_columns,filter)
    display_dbinfo(database,txt_table,filter)
    
    
def display_dbinfo(database,text,filter):
    """_summary_
    Clear the tkinter text field, call get_dbinfo() to get information from the database, then display the information to the user.

    Arguments:
        database -- DatabaseSpecifics class object: holds the database information, connector, and cursor
        text -- tkinter text field: will display the information received from the database.
        filter -- MyFilter class object: holds the selected columns and filter variables.
    """ 
    
    text.config(state=NORMAL)
    text.delete('1.0',END)
    db_info_string = ''
    if not database.isAvailable():
        db_info_string = 'No database loaded.' 
    else:
        db_info_string = get_dbinfo(database,filter)
    
    
    text.insert(END, db_info_string)
    text.config(state=DISABLED)


def table_column_xview(*args):
    """_summary_ Control two related tkinter text fields with one horizontal scroll bar.    """    

    txt_db.xview(*args)
    txt_columnnames.xview(*args)


def AutocompleteOnClick(obj,database):
    """_summary_
    Update the TKinter AutocompleteCombobox completion list when clicked if the completion list is is empty. 

    Arguments:
        obj -- TKinter AutocompleteCombobox widget
        database -- DatabaseSpecifics class object: holds the database information, connector, and cursor
    """    
    
    if obj.full_list == []:
        obj.set_completion_list(database.titles)
    obj.focus_set()

######################### MAIN program ##########################

database = DatabaseSpecifics()
filter = MyFilter(10)
root=Tk() 
# root window title and dimension
root.title("SearcherGUI")

# get user resolution and set geometry 
height, width = get_display_size()
if width >= 1152:
    font = 'Consolas 11'
    winWidth = 1152
elif width < 1152 and width >= 960:
    font = 'Consolas 10'
    winWidth = 960
else:
    font = 'Consolas 10'
    winWidth = width
winHeight = height
geo = str(winWidth)+'x'+str(winHeight)+'+0+0' # start window in top left corner of user screen
root.geometry(geo)

# Change default font type and size
root.option_add( "*font", font)



##### Root Frame Widgets #####
frame_window = Frame(root) 
frame_window.grid(column=0,row=0)

frame_login = Frame(frame_window)
frame_login.grid(column=0,row=0,sticky=W)

frame_databaseinfo = Frame(frame_window)
frame_databaseinfo.grid(column=0,row=1,columnspan=2)

frame_filters = Frame(frame_databaseinfo)
frame_filters.grid(column=0,row=0,columnspan=2)

frame_description = Frame(frame_databaseinfo)
frame_description.grid(column=2,row=0)


##### database login widgets #####
btn_loadDB = Button(frame_login, text = "Load MySQL Database" ,fg = "black",anchor='w', command = lambda: load_database(database))
btn_loadDB.grid(column=0,row=0,sticky='NEWS')
lbl_DB = Label(frame_login, text = 'No database loaded')
lbl_DB.grid(column=1,row=0,sticky='NESW',padx=(10,0))


##### filter widgets #####
btn_updateTable = Button(frame_filters,text="Update Table",command = lambda: update_table(database,txt_db,txt_columnnames,filter))
btn_updateTable.grid(column=0,row=0,rowspan=1,sticky='NESW')
btn_filter = Button(frame_filters, text = "Filter", command = lambda: select_filters(filter))
btn_filter.grid(column = 1, row = 0,rowspan = 1, sticky='NSEW')
btn_columns = Button(frame_filters, text = "Show Columns", command = lambda: select_columns(filter))
btn_columns.grid(column=2,row=0,rowspan=1,sticky='NSWE')


##### media description widgets with autocomplete combobox #####
var_title = StringVar()
title_combo = AutocompleteCombobox(frame_description,textvariable=var_title)
title_combo.grid(column=0,row=1)
title_combo.bind("<1>", lambda event: AutocompleteOnClick(title_combo,database))
btn_description = Button(frame_description,text='Show Description',command = lambda: load_description_info(database,txt_description,var_title,wanttosee_togglebtn,watched_togglebtn,ignored_togglebtn,favorite_togglebtn))
btn_description.grid(column = 1, row = 1)
lbl_title = Label(frame_description,text='Enter Title')
lbl_title.grid(column=0,row=0)
txt_description = scrolledtext.ScrolledText(frame_description,height=23,width=40,wrap=WORD)
txt_description.grid(column=0,row=3,columnspan = 2,rowspan=2,sticky='NEWS')


# want to see toggle
var_wanttosee_state = IntVar()
wanttosee_togglebtn = Checkbutton(frame_description,text='Want To See',variable=var_wanttosee_state,onvalue=1,offvalue=0,command=lambda:toggle_bool_state(database,'want_to_see',var_wanttosee_state,var_title))
wanttosee_togglebtn.grid(column=0,row=5,sticky=W)

# watched toggle
var_watched_state = IntVar()
watched_togglebtn = Checkbutton(frame_description,text='Watched',variable=var_watched_state,onvalue=1,offvalue=0,command=lambda:toggle_bool_state(database,'watched',var_watched_state,var_title))
watched_togglebtn.grid(column=0,row=6,sticky=W)

# ignored toggle 
var_ignored_state = IntVar()
ignored_togglebtn = Checkbutton(frame_description,text='Ignored',variable=var_ignored_state,onvalue=1,offvalue=0,command=lambda:toggle_bool_state(database,'ignored',var_ignored_state,var_title))
ignored_togglebtn.grid(column=0,row=7,sticky=W)

# favorite toggle
var_favorite_state = IntVar()
favorite_togglebtn = Checkbutton(frame_description,text='Favorite',variable=var_favorite_state,onvalue=1,offvalue=0,command=lambda:toggle_bool_state(database,'favorite',var_favorite_state,var_title))
favorite_togglebtn.grid(column=0,row=8,sticky=W)


###### media info table widgets #########
txtHsb = Scrollbar(frame_filters,orient='horizontal',command=table_column_xview)
txtHsb.config(command=table_column_xview)
txtHsb.grid(column=0,row=3,columnspan=10,sticky=EW)

txt_columnnames = Text(frame_filters,height=1,width=90,wrap=NONE, xscrollcommand=txtHsb.set)
txt_columnnames.grid(column=0,row=2,columnspan=10,sticky='NWS')

txt_db = scrolledtext.ScrolledText(frame_filters, height = 30, width = 90,wrap=NONE,xscrollcommand=txtHsb.set)
txt_db.grid(column = 0, row = 4, columnspan = 10,rowspan = 10,sticky='NEWS')
txt_db.insert(END, 'Welcome. Please login to a MySQL database to begin.\n\nDeveloped by Andrew Lopez.\nGithub: https://github.com/alopez8\nItch.io: https://jydin.itch.io/\nDesigned For Use With Dataset: \n    Name: Netflix TV Shows and Movies (titles.csv).\n    Uploaded by: Victor Soeiro.\n    Dataset URL: https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies')
txt_db.config(state=DISABLED)


# Execute Tkinter
root.mainloop() 
