#CreateNetflixDB.py

#parse a .csv file and make a mySQL DB object
#use mysql.connector to connect to the database


#TODO compile and try to build db?



import mysql.connector
from mysql.connector import errorcode
from csv import reader

filename = input('Please enter the /path/to/data/file. Do not include to the file extension (.csv)\n')

try:
    fopen = open('%s.csv' % filename, 'r', encoding='utf8')
except:
    print("Could not open %s.csv file" % filename)
    exit()


sqlhost = input('Please enter the MySQL Host\n')
print("Connecting to MySQL database host '%s'" % sqlhost)
sqluser = input('Please enter your MySQL username\n')
sqlpassword = input('Please enter your MySQL password\n')
dbname = input('Please enter your MySQL database name\n')

print('\nAttempting to connect to %s' %sqlhost)

try:
    mydb = mysql.connector.connect(host=sqlhost,user=sqluser,password=sqlpassword)
except:
    print('Failed to connect to host [%s] as user [%s]' % (sqlhost,sqluser))
    exit()
    
print('Successfully Connected')    
cursor = mydb.cursor()

print('Creating database...')

#drop database
cursor.execute("DROP DATABASE IF EXISTS %s" %dbname)

###create database for netflix database
cursor.execute("CREATE DATABASE IF NOT EXISTS %s" %dbname) 
cursor.execute("USE %s" %dbname) 

#create media table
cursor.execute("""CREATE TABLE IF NOT EXISTS media ( 
               id INTEGER PRIMARY KEY AUTO_INCREMENT, 
               justwatch_id VARCHAR(10) UNIQUE, 
               title VARCHAR(85), 
               media_type ENUM('SHOW','MOVIE'),
               description VARCHAR(2000), 
               release_year SMALLINT, 
               age_certification VARCHAR(8), 
               runtime SMALLINT, 
               imdb_id VARCHAR(10) UNIQUE,
               want_to_see TINYINT, 
               watched TINYINT, 
               ignored TINYINT, 
               favorite TINYINT )
               """)

#CREATE TABLE FOR TV SEASONS, MOVIE ENTRIES HAVE '' AS SEASON 
cursor.execute("""CREATE TABLE IF NOT EXISTS seasons (
    media_id INTEGER PRIMARY KEY,
    numseasons INTEGER,
    FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE)
    """)

#CREATE TABLE FOR TMDB_POPULARITY,TMDB_SCORE
cursor.execute("""CREATE TABLE IF NOT EXISTS tmdb_info (
    media_id INTEGER PRIMARY KEY,
    tmdb_popularity DECIMAL(8,3),
    tmdb_score DECIMAL(5,3),
    FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE)
    """)

#CREATE TABLE FOR IMDB_ID,IMDB_SCORE,IMDB_VOTES
cursor.execute("""CREATE TABLE IF NOT EXISTS imdb_info (
    imdb_id VARCHAR(10) PRIMARY KEY,
    imdb_score DECIMAL(2,1),
    imdb_votes INTEGER,
    FOREIGN KEY (imdb_id) REFERENCES media (imdb_id) ON DELETE CASCADE)
    """)

#CREATE GENRE TABLE
cursor.execute("""CREATE TABLE IF NOT EXISTS genre (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    genre_name ENUM('documentation', 'drama', 'sport', 'romance', 'comedy', 'crime', 'music', 'fantasy', 'european', 'thriller', 'action', 'history', 'family', 'war', 'animation', 'scifi', 'reality', 'western', 'horror','') UNIQUE)
    """)


#CREATE MEDIA-GENRE JOINT TABLE
cursor.execute("""CREATE TABLE IF NOT EXISTS media_genre (
    media_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre (id) ON DELETE CASCADE,
    PRIMARY KEY (media_id,genre_id))
    """)

#CREATE PRODUCTION_COMPANY TABLE 
cursor.execute("""CREATE TABLE IF NOT EXISTS country (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    country_name CHAR(2) UNIQUE)
    """)

#CREATE PRODCOM-MEDIA JOINT TABLE
cursor.execute("""CREATE TABLE IF NOT EXISTS media_country (
    media_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES country (id) ON DELETE CASCADE,
    PRIMARY KEY (media_id, country_id) )
    """)


### read in info from .csv
counter = 0

justwatchid = ''
mediatitle = ''
media_type = ''
media_desc = ''
year = 0
age_cert = ''
duration = 0
want = False
watched = False
ignore = False
favorite = False
imdbid = ''
imdbscore = 0
imdbvotes = 0
tmdbpop = 0
tmdbscore = 0


for line in reader(fopen,delimiter=",",quotechar='"'):
    counter += 1    
    if counter == 1:
        continue

    #update media info variables
    justwatchid = line[0]
    mediatitle = line[1]
    media_type = line[2]
    media_desc = line[3]
    year = int(line[4])
    age_cert = line[5]
    duration = int(line[6])
    genres = line[7].replace("'","").replace("[","").replace("]","").split(', ')   
    pclist = line[8].replace("'","").replace("[","").replace("]","").split(", ")
    numseasons = line[9]
    imdbid = line[10]
    imdbscore = line[11]
    if imdbscore != '':
        imdbscore = float(imdbscore)
    imdbvotes = line[12]
    if imdbvotes != '':
        imdbvotes = int(float(imdbvotes))
    tmdbpop = line[13]
    if tmdbpop != '':
        tmdbpop = float(tmdbpop)
    tmdbscore = line[14]
    if tmdbscore != '':
        tmdbscore = float(tmdbscore)

        
    #END OF LOOP, INSERT INFO INTO TABLES
    
    #MEDIA TABLE
    #insert into media table
    cursor.execute("""INSERT INTO media 
                   VALUES (NULL,%s,%s,%s,%s,%s,NULLIF(%s,''),%s,NULLIF(%s,''),%s,%s,%s,%s)""", 
                   (justwatchid, mediatitle, media_type, media_desc, year, age_cert, duration, imdbid,want, watched, ignore, favorite)
                   ) 
    
    #get id from media table
    cursor.execute("SELECT id from media WHERE justwatch_id = %s",(justwatchid,))
    media_id = cursor.fetchall()[0][0]
    
    #GENRE & MEDIA_GENRE TABLE
    for i in genres:
        #insert into genre table
        cursor.execute("""
                       INSERT INTO genre (genre_name)
                       SELECT * FROM (SELECT %s) AS tmp
                       WHERE NOT EXISTS (
                           SELECT genre_name FROM genre WHERE genre_name = %s
                       ) LIMIT 1;
                        """, (i,i)
                        )    
        #get id from genre table
        cursor.execute("SELECT id FROM genre WHERE genre_name = %s",(i,))
        genre_id = cursor.fetchall()[0][0]
        
        #insert into join media_genre table
        cursor.execute("""
                       INSERT INTO media_genre
                       VALUES (%s,%s)
                       """, (media_id,genre_id)
                       )
    
    #COUNTRY TABLE & MEDIA_COUNTRY TABLE
    for i in pclist:
        #insert into country table if country does not already exist
        cursor.execute("""
                       INSERT INTO country (country_name)
                       SELECT * FROM (SELECT %s) as tmp
                       WHERE NOT EXISTS (
                           SELECT country_name FROM country WHERE country_name = %s
                        ) LIMIT 1;
                        """, (i,i)
                       )
        #get country_id from country table
        cursor.execute("SELECT id from country WHERE country_name = %s",(i,))
        country_id = cursor.fetchall()[0][0]
        
        #insert into association media_country table
        cursor.execute("""
                       INSERT INTO media_country
                       VALUES (%s,%s)
                       """,(media_id,country_id)
                       )
    
    #SEASONS TABLE
    #insert into the seasons table
    if numseasons != '':
        numseasons = int(float(numseasons))
        #INSERT INTO seasons table (media_id, numseasons)
        cursor.execute("""
                       INSERT INTO seasons
                       VALUES (%s,%s)
                       """, (media_id,numseasons)
                       )


    #IMDB_INFO TABLE
    #insert into imdb_info table
    if imdbid != '':
        cursor.execute("""
                        INSERT INTO imdb_info
                        VALUES (%s,NULLIF(%s,''),NULLIF(%s,''))
                        """, (imdbid,imdbscore,imdbvotes)
                    )
    
    #TMDB_INFO TABLE
    #insert into tmdb_info table
    cursor.execute("""
                   INSERT INTO tmdb_info
                   VALUES (%s,NULLIF(%s,''),NULLIF(%s,''))
                   """, (media_id,tmdbpop,tmdbscore)
                   )
    


#save
mydb.commit()
#disconnect from database
cursor.close()
mydb.close()

print("Program Finished")
