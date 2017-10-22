#  Skew-T-map-projector - v0.2
 
INDEX  
1- CONTENT OF FOLDER  
2- IDEA OF SCRIPT  
3- MISSING PACKAGES INSTALLATION  
5- SETTING FOLDER  
6- USE OF SCRIPT  

CONTENT OF FOLDER  
html/ contains the html files if you manually download them. They are parsed from the script to become .txt data files. If you use it, you can choose to use 'save html only' when saving the sounding's webpage.  

soundings/ contains the .txt data files to draw the map. It contains subfolders in the format '091017-00' meaning Oct 9th 2017, Z00.  

README.md is this file.  

setup.py is the first script you have to use, to install all the needed missing packages. You need to run it only once.  

folders_setup.py is the second script you need to use. It allows you to define the path of *this* folder. You can run it once or whenever you need to change the location of *this* folder.  

path_variables.py is a variable definition script, which is modified by folders_setup.py.  

skew-T.py is the main script, that prints data from soundings on the map.  

IDEA OF SCRIPT  
## This program reads the latitude and ID number of stations from which soundings are usually available. They are reported in file stations_loc.txt in this folder.

Setting variables 'year', 'month', 'day' and 'hour' allows to select the soundings.

folder_path variable indicates the folder in which html pages are saved and from which the program converts the data to txt before reading them. At the moment data download is manual, planning to make it automatic in the next future. Path should be changed until the 'maps' folder, which contains this script.

Next 'for' iteration reads inside station_ID array, to open the 'url' html file, convert it to .txt format and save it inside a file located in the 'soundings' subfolder. .txt formatted data are archived by date and time.
Nested 'for' cycle (around line 60) comments with a '#' lines for which not all data are available in the columns. This isn't a very clever idea, I admit, but running the program all at once, I couldn't find anything more useful to get rid of extraction errors.

Next 'for' cycle opens the txt soundings' files and saves data into multidimensional arrays (being at the moment just for geopotential height at 500 hPa).

Last lines plot on a mercator projected map of Europe dots representing the location of stations and altitude of reading with the associated label.

TO DO LIST:  
    - automatic data mining from wyoming university website (or other indication). This requires an automatic check for unavailable soundings that does not end in script's error stop.  
    - color gradient data representation for heights, temperatures humidity and other scalar quantities.  
    - vector representation of vectorial quantities such as wind, pressure gradients or temperature gradients. This obviously requires a defined function for extracting gradients in a useful way.  
    - create installer to check for missing packages and to install them. It should also verify folder paths and create/change/update them.  
    - define different functions and (eventually) create a library to decide which type of data display or to display all data at once on different/same plot.  
