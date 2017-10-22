#  Skew-T-map-projector - v0.2
 
#	INDEX
#	1- IDEA OF SCRIPT
#	2- MISSING PACKAGES INSTALLATION
#	3- SETTING FOLDER
#	4- USE OF SCRIPT

This program reads the latitude and ID number of stations from which soundings are usually available. They are reported in file stations_loc.txt in this folder.

Setting variables 'year', 'month', 'day' and 'hour' allows to select the soundings.

## folder_path variable indicates the folder in which html pages are saved and from which the program converts the data to txt before reading them. At the moment data download is manual, planning to make it automatic in the next future. Path should be changed until the 'maps' folder, which contains this script.

Next 'for' iteration reads inside station_ID array, to open the 'url' html file, convert it to .txt format and save it inside a file located in the 'soundings' subfolder. .txt formatted data are archived by date and time.
Nested 'for' cycle (around line 60) comments with a '#' lines for which not all data are available in the columns. This isn't a very clever idea, I admit, but running the program all at once, I couldn't find anything more useful to get rid of extraction errors.

Next 'for' cycle opens the txt soundings' files and saves data into multidimensional arrays (being at the moment just for geopotential height at 500 hPa).

Last lines plot on a mercator projected map of Europe dots representing the location of stations and altitude of reading with the associated label.

TO DO LIST:
    - automatic data mining from wyoming university website (or other indication). This requires an automatic check for unavailable soundings that does not end in script's error stop.
    - color gradient data representation for heights, temperatures humidity and other scalar quantities
    - vector representation of vectorial quantities such as wind, pressure gradients or temperature gradients. This obviously requires a defined function for extracting gradients in a useful way.
    - create installer to check for missing packages and to install them. It should also verify folder paths and create/change/update them.
    - define different functions and (eventually) create a library to decide which type of data display or to display all data at once on different/same plot.
