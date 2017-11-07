from urllib.request import urlopen
from bs4 import BeautifulSoup
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy
import pylab
import os

from path_variables import *
plt.close()

station_lat, station_lon, station_ID = numpy.loadtxt(stationloc_folder, unpack=True)
lat, lon, IDs = station_lat, station_lon, station_ID

## INSERT DATA BELOW
year  = '17'
month = '11'
day   = '06'
hour  = '12' #either 12 or 00
## INSERT DATA ABOVE

folder_path = soundings_folder + str(day)+str(month)+str(year)+'-'+str(hour)+'\\'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

i = 0
for stn in station_ID:
    if len(str(int(stn))) < 5:
        stn = '0' + str(int(stn))
    else:
        stn = str(int(stn))

    ## 1) Wyoming URL to download Sounding from
    url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR='+year+'&MONTH='+month+'&FROM='+day+hour+'&TO='+day+hour+'&STNM='+stn
    content = urlopen(url).read()

    ## 2) Remove the html tags
    soup = BeautifulSoup(content)
    data_text = soup.get_text()
        
    if (data_text[1:4] != 'Can'):
    ## 3) Split the content by new line.
        splitted = data_text.split("\n",data_text.count("\n"))

    ## 4) Write this splitted text to a .txt document
        Sounding_filename = str(stn)+'.txt'
        data_path = folder_path + Sounding_filename
    
        f = open(data_path,'w')
        for line in splitted[4:10]:
            f.write('#'+line+'\n')
        
        for line in splitted[10:-52]:
            if (line[0]!=' '):
                    break
            elif (line[4] == ' '):
                break
            else:
                f.write(line[0:7])
                    
                if (line[13] == ' '):
                    f.write(line[7:9]+'-9999')
                else:
                    f.write(line[7:14])
                    
                if (line[18] == ' '):
                    f.write(line[14:16]+'-9999')
                else:
                    f.write(line[14:21])
                    
                if (line[25] == ' '):
                    f.write(line[21:23]+'-9999')
                else:
                    f.write(line[21:28])
                    
                if (line[34] == ' '):
                    f.write(line[28:30]+'-9999')
                else:
                    f.write(line[28:35])
                    
                if (line[38] == ' '):
                    f.write(line[35:37]+'-9999')
                else:
                    f.write(line[35:42])
                    
                if (line[48] == ' '):
                    f.write(line[42:44]+'-9999')
                else:
                    f.write(line[42:49])
                
                if (line[55] == ' '):
                    f.write(line[49:52]+'-9999')
                else:
                    f.write(line[49:56])
                    
                if (line[58] == ' '):
                    f.write(line[56:58]+'-9999')
                else:
                    f.write(line[56:63])
                    
                if (line[65] == ' '):
                    f.write(line[63:65]+'-9999')
                else:
                    f.write(line[63:70])
                    
                if (line[72] == ' '):
                    f.write(line[70:72]+'-9999')
                else:
                    f.write(line[70:])
                    
                f.write('\n')
        f.close()
        i+=1
    else:
        lat = numpy.delete(lat, i)
        lon = numpy.delete(lon, i)
        IDs = numpy.delete(IDs, i)

stations_filename  = 'availables.txt'
availstations_path = folder_path + stations_filename

f = open(availstations_path,'w')
f.write('#Lat\tLon\tID\n')
for i in range(len(IDs)):
    f.write(str(lat[i])+'\t'+str(lon[i])+'\t'+str(int(IDs[i]))+'\n')
f.close()