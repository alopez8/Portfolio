README

---------------------------------------------------------

Author:
Andrew Lopez

Finish Date:
May 18, 2023

Project Title:
Searcher GUI

---------------------------------------------------------

Project Description:
Create a MySQL database that contains the netflix library. Create a GUI to search, apply filters, and change the database with the purpose of helping the user navigate the netflix library.
Developed on a Windows 10 PC with resolution 1920x1080 and a local MySQL server.

CreateDB.py contains the program which creates a MySQL database from a kaggle dataset (.csv).
CreateDB requires the dataset (.csv) have a very specific format.

SearcherGUI.py contains the main program which allows the user to navigate and update the database.
SearcherGUI.py can load a MySQL database (See below for Database Structure). Once loaded the user can select which columns to display and/or can apply fourteen different filters. Additionally, the user can use a side panel to fetch the description of a specific title. Once the description has been retrieved, the user can update four columns (via checkboxes): 1. Want to See, 2. Watched, 3. Ignored, 4. Favorite. These column updates are immediately pushed to the database allowing the user to use these values in filters without having to reload the program or database.

Used tkinter library to build the gui.
Used mysql.connector to connect to the MySQL server and perform queries on the database.
Used pyinstaller to create a one file executable to run on windows.

Used dataset https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies uploaded by: Victor Soeiro. Other streaming datasets uploaded by Victor Soeiro with similarly formatted titles.csv SHOULD also be compatible with this project. This has not been tested.

---------------------------------------------------------

Goals:

The primary goals of this project were
1. To practice creating a GUI using python,
2. To learn how to construct a RDBMS database using MySQL,
3. To learn how to normalize a Relational database,
4. To learn how to access and alter a RDBMS database using MySQL queries,
5. To gain experience developing a program from beginning to end,
6. To practice general python skills.

---------------------------------------------------------


What I Learned:

During this project I learned how to design and normalize a Relational database. I also learned MySQL syntax and practiced assembling queries.
Additionally I learned how to connect to and alter a MySQL database using Python 3.
I practiced developing and working with classes in Python 3.


Difficulties:

The most difficult part of this project was working with the Relational database. Before starting I did not have a good understanding of how databases are designed (e.g. expressing and calling many-to-many relationships) nor did I know what database normalization meant. I also expected and experienced a few difficulties with the MySQL syntax which was entirely new to me.
I ran into a few other problems during development. As I kept adding new filters the number of variables I was passing around kept expanding. I eventually refactored these filter variables into a class object of my design. I also spent time refactoring my code to prevent function bloat. Lastly, due to the number of filters and columns that I allow the user to access, it was difficult testing the program for bugs, specifically testing that the MySQL query is correctly assembled.


---------------------------------------------------------


Usage:
0. Acquire titles.csv from the kaggle dataset. https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies

Use CreateDB.py and titles.csv to create a MySQL Relational Database. 
1. Enter the path to the datafile without the extension.
2. Enter the MySQL Hostname
3. Enter the MySQL username
4. Enter the MySQL user password
5. Enter the preferred name of the database. This will overwrite any existing database of the same name.


SearcherGUI.py
1. Click the 'Load MySQL Database' button to pull up the login window.
2. In the login window, enter the MySQL host name, database name (created by CreateDB.py), username, and user password. Click 'Login' to complete the connection.
3. Check the message next to the 'Load MySQL Database' button. If the database failed to connect, then return to Step 1. Otherwise, continue to either Step 4 or Step 7 as desired.

# Using the table
4. (Optional) Click the 'Filter' button to bring up a window showing which filters can be applied to the database. Apply the selected filters with the 'Apply' button.
5. (Optional) Click the 'Show Columns' button to bring up a window showing the database columns which can be displayed or hidden. Click the checkbox of each column the user wishes to display then click 'Apply'.
6. Click 'Update Table' to update the information display, applying any 'Filter' or 'Show Columns' changes to the table.  

# Using the description box
7. After connecting to the database, click the entry box next to the 'Show Description' button. The user may now view all media titles in the dropdown menu. This Entry box also features autocomplete. By typing in the entry box, the dropdown menu will remove any media titles that do not match.
8. Once a media title has been selected with the entry box, click 'Show Description' to display the title and description of the selected media.
9. While the description is displayed, the user can toggle whether they 'Want to See' this title, have already 'Watched' this title, wish to 'Ignore' this title, or if this title is a 'Favorite' by clicking the appropriate checkbox. As soon as a box is checked/unchecked the database is updated and saved. The user may need to click 'Update Table' to properly filter these categories in the information display.


---------------------------------------------------------

Installation:

Install CreateDB.py with pyinstaller using the command:
    $ pyinstaller --noconsole --onefile --console CreateDB.py

Install SearcherGUI.py with pyinstaller using the command: 
    $ pyinstaller --noconsole --onefile SearcherGUI.py

---------------------------------------------------------

Database Design:

The database is made up of eight tables. 
Most of the information is held in the 'media' table.

There are also three tables which have been separated from the media table due to large amounts of NULL data.
The 'seasons' table holds the number of seasons for each media entry.
The 'tmdb_info' table holds the Score and Popularity of each media entry as listed on www.themoviedb.org
The 'imdb_info' table holds the Score and Votes of each media entry as listed on www.imdb.com

Additionally there are four tables which display N-N relationships (media genre, media production country)
The table 'genre' and the association table 'media_genre' contain information about the listed genres of each media entry.
The table 'country' and the association table 'media_country' contain information about the listed production countries for each media entry.

Below are the MySQL Queries that create each table

# create media table
CREATE TABLE IF NOT EXISTS media ( 
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
               favorite TINYINT 
               )

# create table for TV seasons, movie entries have '' as season 
CREATE TABLE IF NOT EXISTS seasons (
    media_id INTEGER PRIMARY KEY,
    numseasons INTEGER,
    FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE
    )

# create table for tmdb popularity and score
CREATE TABLE IF NOT EXISTS tmdb_info (
    media_id INTEGER PRIMARY KEY,
    tmdb_popularity DECIMAL(8,3),
    tmdb_score DECIMAL(5,3),
    FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE
    )

# create table for imdb score and votes
CREATE TABLE IF NOT EXISTS imdb_info (
    imdb_id VARCHAR(10) PRIMARY KEY,
    imdb_score DECIMAL(2,1),
    imdb_votes INTEGER,
    FOREIGN KEY (imdb_id) REFERENCES media (imdb_id) ON DELETE CASCADE
    )

# create genre table
CREATE TABLE IF NOT EXISTS genre (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    genre_name ENUM('documentation', 'drama', 'sport', 'romance', 'comedy', 'crime', 'music',
        'fantasy', 'european', 'thriller', 'action', 'history', 
        'family', 'war', 'animation', 'scifi', 'reality', 'western', 
        'horror','') UNIQUE
    )

# create media-genre association table
CREATE TABLE IF NOT EXISTS media_genre (
    media_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre (id) ON DELETE CASCADE,
    PRIMARY KEY (media_id,genre_id)
    )

# create production country table 
CREATE TABLE IF NOT EXISTS country (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    country_name CHAR(2) UNIQUE
    )

# create media-production country association table
CREATE TABLE IF NOT EXISTS media_country (
    media_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES country (id) ON DELETE CASCADE,
    PRIMARY KEY (media_id, country_id) 
    )

---------------------------------------------------------

LICENSE/COPYING: 
This project is licensed under the GNU General Public License v3.0 (GNU GPLv3) URL: https://www.gnu.org/licenses/gpl-3.0.en.html 
See LICENSE.md for the full text of the license.
