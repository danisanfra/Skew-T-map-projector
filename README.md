
#  Skew-T map-projector - v0.3
 
## INDEX  
##### 1. CONTENT OF FOLDER   
##### 2. MISSING PACKAGES INSTALLATION   
##### 3. TO DO LIST  

## 1. CONTENT OF FOLDER  
html/ contains the html files if you manually download them. They are parsed from the script to become .txt data files. If you use it, you can choose to use 'save html only' when saving the sounding's webpage. It contains a demo subfolder in the format '091017-00' meaning Oct 9th 2017 Z00, which is the format you should use to save your html pages.  

soundings/ contains the .txt data files to draw the map. It contains subfolders in the format '091017-00' as before. It contains some demo files to test the software and if the needed packages are correctly installed.  

README.md is this file.  

path_variables.py is a variable definition script, which is to be modified the first time you use the software and any time you change its path.  What you need to insert in the 'maps_folder' variable is the absolute path to the inside of your 'Skew-T-map-projector' folder.  

data_manual.py is the script that allows you to convert your html files into .txt data, saved inside the 'soundings' subfolder. You have to pay attention to insert the correct date and time.

data_downloader.py automatically downloads and converts html soundings' data and saves them into the 'soundings' subfolder. You have to insert the correct date and time as well.  

map.py is the main script. After typing the correct date and time and the pressure level you want to analyze, it plots a double map of Europe, showing height of radiosonde at given pressure, wind and temperature both for wet bulb and dry bulb.  

## 2.MISSING PACKAGES INSTALLATION  
    - urllib: needed for urlopen to open url paths both from local folder and from the internet  
    - bs4: needed for BeautifulSoup, to remove the html tags before converting it to .txt file.  
    - os: should be already installed by default.  
    - numpy: needed for data extraction and analysis.  
    - matplotlib: needed for plotting data.  
    - basemap: needed for geographical maps. Follow instructions at ```https://matplotlib.org/basemap/users/installing.html```.  
    - pillow: it's only suggested by basemap, but it is used for orographic maps.  
    - goes: you need to install it during basemap installation.  
 
In general ```https://www.lfd.uci.edu/~gohlke/pythonlibs/``` may be a good page to look for windows binaries.  

## 3. TO DO LIST:  
    - vector representation of vectorial quantities such as pressure gradients or temperature gradients. This obviously requires a defined function for extracting gradients in a useful way.  
    - define different functions and (eventually) create a library to decide which type of data display or to display all data at once on different/same plot.  
