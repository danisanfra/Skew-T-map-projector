from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy
import os

from path_variables import *

# station_loc contains some stations for Europe. Some of them are commented out because it seems that they haven't transmitted data for a while. The three copies are used because the program checks for invalid datasets, removing the corresponding station from the plot.
station_lat, station_lon, station_ID = numpy.loadtxt(stationloc_folder, unpack=True)
lat, lon, IDs = station_lat, station_lon, station_ID

## INSERT DATA BELOW
year  = '17'
month = '10'
day   = '09'
hour  = '00' #either 12 or 00
## INSERT DATA ABOVE

# checks for existence of folder for the given date and time. If it does not exist, it is created, otherwise it is updated running the script.
folder_path = soundings_folder + str(day)+str(month)+str(year)+'-'+str(hour)+'\\'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# runs through the known stations. If the analized station's html file exists, it is converted into a txt file. Empty columns are filled with a -9999 code, so that if some data is missing, it may be still possible to plot what is available. If pressure is unavailable, the whole line is deleted, since this plot is based on pressure levels. In case the html file does not exist, conversion is stopped and the corresponding station is deleted from auxiliary arrays lat, lon and IDs.
i = 0
for stn in station_ID:
    generate_data = True
    if len(str(int(stn))) < 5:
        stn = '0' + str(int(stn))
    else:
        stn = str(int(stn))
    url = url_folder + '\\' + str(day)+str(month)+str(year)+'-'+str(hour) + '\\' + stn + '-' + day + month + year + '-' + hour + '.html'

    # 1) url of sounding for already downloaded html file (above is path).
    try:
        content = urlopen(url).read()
    except:
        lat = numpy.delete(lat, i)
        lon = numpy.delete(lon, i)
        IDs = numpy.delete(IDs, i)
        generate_data = False
        
    if generate_data == True:
        # 2) Remove the html tags.
        soup = BeautifulSoup(content)
        data_text = soup.get_text()
        
        # 3) Split the content by new line.
        splitted = data_text.split("\n",data_text.count("\n"))
    
        # 4) Write this splitted text to a txt document.
        Sounding_filename = str(stn)+'.txt'
        data_path = folder_path + Sounding_filename

    	# jumps heading lines.
        f = open(data_path,'w')
        for line in splitted[4:10]:
            f.write('#'+line+'\n')

        # conversion of lines containing data.
        for line in splitted[10:-52]:
            if (line[0]!=' '):				# end of dataset.
                    break
            elif (line[4] == ' '):			# pressure is missing.
                break
            else:
                f.write(line[0:7])
                    
                if (line[13] == ' '):
                    f.write(line[7:9]+'-9999')		# height is missing.
                else:
                    f.write(line[7:14])
                    
                if (line[18] == ' '):
                    f.write(line[14:16]+'-9999')	# dry bulb temperature is missing.
                else:
                    f.write(line[14:21])
                    
                if (line[25] == ' '):
                    f.write(line[21:23]+'-9999')	# wet bulb temperature is missing.
                else:
                    f.write(line[21:28])
                    
                if (line[34] == ' '):
                    f.write(line[28:30]+'-9999')	# relative humidity is missing.
                else:
                    f.write(line[28:35])
                    
                if (line[38] == ' '):
                    f.write(line[35:37]+'-9999')	# mixture is missing.
                else:
                    f.write(line[35:42])
                    
                if (line[48] == ' '):
                    f.write(line[42:44]+'-9999')	# wind direction is missing.
                else:
                    f.write(line[42:49])
                
                if (line[55] == ' '):
                    f.write(line[49:52]+'-9999')	# wind speed [knots] is missing.
                else:
                    f.write(line[49:56])
                    
                if (line[58] == ' '):
                    f.write(line[56:58]+'-9999')	# THTA is missing.
                else:
                    f.write(line[56:63])
                    
                if (line[65] == ' '):
                    f.write(line[63:65]+'-9999')	# THTE is missing.
                else:
                    f.write(line[63:70])
                    
                if (line[72] == ' '):
                    f.write(line[70:72]+'-9999')	# THTV is missing.
                else:
                    f.write(line[70:])
                    
                f.write('\n')				# end of line.
        f.close()
        i+=1		# increases the counter for the auxiliary arrays lat, lon and IDs.

# Creates a file inside the soundings' folder with the available stations for given date and time.
stations_filename  = 'availables.txt'
availstations_path = folder_path + stations_filename

f = open(availstations_path,'w')
f.write('#Lat\tLon\tID\n')
for i in range(len(IDs)):
    f.write(str(lat[i])+'\t'+str(lon[i])+'\t'+str(IDs[i])+'\n')
f.close()
