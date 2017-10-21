from urllib.request import urlopen
from bs4 import BeautifulSoup

from mpl_toolkits.basemap import Basemap
"""
Skew-T map projector - v0.1

This program reads the latitude and ID number of stations from which soundings are usually available. They are reported in file stations_loc.txt. 

Variables 'year', 'month', 'day' and 'hour' are set for the soundings.
folder_path variable indicates the folder in which html pages are saved and from which the program converts the data to txt before reading them. At the moment data download is manual, planning to make it automatic in the next future. Path should be changed until the 'maps' folder, which contains this script.

Next 'for' iteration reads inside station_ID array, to open the 'url' html file, convert it to .txt format and save it inside a file located in the 'soundings' subfolder. .txt formatted data are archived by date and time.
Nested 'for' cycle (around line 60) comments with a '#' lines for which not all data are available in the columns. This isn't a very clever idea, I admit, but running the program all at once, I couldn't find anything more useful to get rid of extraction errors.

Next 'for' cycle opens the txt soundings' files and saves data into multidimensional arrays (being at the moment just for geopotential height at 500 hPa).

Last lines plot on a mercator projected map of Europe dots representing the location of stations and altitude of reading with the associated label.

TO DO LIST:
    - automatic data mining from wyoming university website (or other indication). This requires an automatic check for unavailable soundings that does not end in script's error stop.
    - color gradient data representation for heights, temperatures humidity and other scalar quantities
    - vector representation of vectorial quantities such as wind, pressure gradients or temperature gradients. This obviously requires a defined function for extracting gradients in a useful way.
    - create installer to check for missing packages and to install them
    - define different functions and (eventually) create a library to decide which type of data display or to display all data at once on different/same plot.
"""

import matplotlib.pyplot as plt
import numpy
import pylab

import os

plt.close()

station_lat, station_lon, station_ID = pylab.loadtxt('C:\\Users\\Daniele\\Desktop\\UNIVERSITA\'\\Atmosfera\\maps\\stations_loc.txt', unpack=True)

year  = '17'
month = '10'
day   = '09'
hour  = '00' #either 12 or 00

folder_path = 'C:\\Users\\Daniele\\Desktop\\UNIVERSITA\'\\Atmosfera\\maps\\soundings\\'+str(day)+str(month)+str(year)+'-'+str(hour)+'\\'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

for stn in station_ID:
    if len(str(int(stn))) < 5:
        stn = '0' + str(int(stn))
    else:
        stn = str(int(stn))
    url = 'file:///C:\\Users\\Daniele\\Desktop\\UNIVERSITA\'\\Atmosfera\maps\\html\\' + stn + '-' + day + month + year + '-' + hour + '.html'

## 1) Wyoming URL to download Sounding from / from already downloaded html file (above is path)
# url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR='+year+'&MONTH='+month+'&FROM='+day+hour+'&TO='+day+hour+'&STNM='+stn
    content = urlopen(url).read()

## 2) Remove the html tags
    soup = BeautifulSoup(content)
    data_text = soup.get_text()

## 3) Split the content by new line.
    splitted = data_text.split("\n",data_text.count("\n"))

## 4) Write this splitted text to a .txt document
    Sounding_filename = str(stn)+'.txt'
    data_path = folder_path + Sounding_filename

    f = open(data_path,'w')
    for line in splitted[4:10]:
        f.write('#'+line+'\n')
    
#     i = 4
    for line in splitted[10:-52]:
        if (line[0]!=' '):
                break
        elif (line[3] == 0 ):
                break
        else:
            if (line[12] == ' '):
                f.write('#'+line+'\n')
            elif (line[18] == ' '):
                f.write('#'+line+'\n')
            elif (line[25] == ' '):
                f.write('#'+line+'\n')
            elif (line[34] == ' '):
                f.write('#'+line+'\n')
            elif (line[38] == ' '):
                f.write('#'+line+'\n')
            elif (line[48] == ' '):
                f.write('#'+line+'\n')
            elif (line[55] == ' '):
                f.write('#'+line+'\n')
            elif (line[58] == ' '):
                f.write('#'+line+'\n')
            elif (line[65] == ' '):
                f.write('#'+line+'\n')
            elif (line[72] == ' '):
                f.write('#'+line+'\n')
            else:
                f.write(line+'\n')
        

        
#         i+=1
    
#     for line in splitted[i:]:
#         if (line[27:43]=='Station latitude'):
#             station_lat = float(line[45:])
#         if (line[26:43]=='Station longitude'):
#             station_lon = float(line[45:])
    
    
    f.close()

geop_height = numpy.empty(len(station_ID))
i = 0
for stn in station_ID:
    if len(str(int(stn))) < 5:
        stn = '0' + str(int(stn))
    else:
        stn = str(int(stn))
        
    Sounding_filename = stn + '.txt'
    data_path = folder_path + Sounding_filename

    data = numpy.array(11)
    data = pylab.loadtxt(data_path, unpack=True)
    
    geop_height[i] = data[1][data[0]==500.0]
    i+=1
    
# wind_dir    = data[6][data[0]==500.0] + 180
# wind_speed  = data[7][data[0]==500.0]

# u10 = wind_speed*pylab.sin(pylab.deg2rad(wind_dir))
# v10 = wind_speed*pylab.cos(pylab.deg2rad(wind_dir))

map = Basemap(llcrnrlon=-10.,llcrnrlat=32,urcrnrlon=40,urcrnrlat=64,resolution=None,projection='tmerc',lon_0=10,lat_0=55)
map.shadedrelief()

map.drawmeridians(numpy.arange(0,360,10), labels=[0,0,0,1],fontsize=10)
map.drawparallels(numpy.arange(-90,90,10), labels=[1,0,0,0], fontsize=10)

x,y = map(station_lon, station_lat)
points = numpy.meshgrid(y, x)

# map.barbs(x[points], y[points], u10[points], v10[points], pivot='middle', barbcolor='#333333')
# map.barbs(x, y, u10, v10, pivot='middle', barbcolor='#333333', length=5)
# map.quiver(x[points], y[points], u10[points], v10[points], speed[points], cmap=plt.cm.autumn)
# map.quiver(x, y, u10, v10, wind_speed, cmap=plt.cm.autumn)

labels = numpy.empty(len(geop_height))

for i in range(len(geop_height)):
    labels[i] = str(geop_height[i])

for labels, xpt, ypt in zip(labels, x, y):
    plt.text(xpt+10000, ypt+5000, labels, fontsize = 8)

map.plot(x, y, 'bo', markersize=1)

plt.show()
