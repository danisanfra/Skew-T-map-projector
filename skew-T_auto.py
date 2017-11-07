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
lat, lon, ID = station_lat, station_lon, station_ID

year  = '17'
month = '10'
day   = '09'
hour  = '00' #either 12 or 00

folder_path = soundings_folder + str(day)+str(month)+str(year)+'-'+str(hour)+'\\'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

i = 0
for stn in station_ID:
    if len(str(int(stn))) < 5:
        stn = '0' + str(int(stn))
    else:
        stn = str(int(stn))
    # url = url_folder + stn + '-' + day + month + year + '-' + hour + '.html'

    ## 1) Wyoming URL to download Sounding from / from already downloaded html file (above is path)
    url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR='+year+'&MONTH='+month+'&FROM='+day+hour+'&TO='+day+hour+'&STNM='+stn
    content = urlopen(url).read()

    ## 2) Remove the html tags
    soup = BeautifulSoup(content)
    data_text = soup.get_text()
        
    if (data_text[1:4] == 'Can'):
        lat = numpy.delete(lat, i)
        lon = numpy.delete(lon, i)
        IDs = numpy.delete(IDs, i)
        i+=1
        break

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


Pressure_level = 500.0

geop_height = numpy.empty(len(IDs));   stat_height = numpy.empty([len(IDs),2])
wind_dir    = numpy.empty(len(IDs));   stat_wind   = numpy.empty([len(IDs),2])
wind_speed  = numpy.empty(len(IDs))
dryT        = numpy.empty(len(IDs));   stat_drtemp = numpy.empty([len(IDs),2])
dewT        = numpy.empty(len(IDs));   stat_wetemp = numpy.empty([len(IDs),2])

i = 0
for stn in IDs:
    if len(str(int(stn))) < 5:
        stn = '0' + str(int(stn))
    else:
        stn = str(int(stn))
        
    Sounding_filename = stn + '.txt'
    data_path = folder_path + Sounding_filename

    data = numpy.array(11)
    data = numpy.loadtxt(data_path, unpack=True)
    
    stat_height[i] = lon[i], lat[i]
    stat_wind[i]   = lon[i], lat[i]
    stat_drtemp[i] = lon[i], lat[i]
    stat_wetemp[i] = lon[i], lat[i]
    
    if (data[1][data[0] == Pressure_level] == -9999.):
        geop_height    = numpy.delete(geop_height, i)
        stat_height    = numpy.delete(stat_height, i, 0)
    else:
        geop_height[i] = data[1][data[0]==Pressure_level]
    
    if (data[6][data[0]==Pressure_level] == -9999. or data[7][data[0]==Pressure_level] == -9999.):
        wind_dir       = numpy.delete(wind_dir, i)
        wind_speed     = numpy.delete(wind_speed, i)
        stat_wind      = numpy.delete(stat_windir, i, 0)
    else:
        wind_dir[i]    = data[6][data[0]==Pressure_level] + 180
        wind_speed[i]  = data[7][data[0]==Pressure_level]
        
    if (data[2][data[0]==Pressure_level] == -9999.):
        dryT           = numpy.delete(dryT, i)
        stat_drtemp    = numpy.delete(stat_drtemp, i, 0)
    else:
        dryT[i]        = data[2][data[0]==Pressure_level]
    
    if (data[3][data[0]==Pressure_level] == -9999.):
        dewT           = numpy.delete(dewT, i)
        stat_wetemp    = numpy.delete(stat_wetemp, i, 0)
    else:
        dewT[i]        = data[3][data[0]==Pressure_level]
        
    i+=1


geop_height /= 1000 #m to km conversion factor
wind_speed  *= 1.85 #knots to km/h conversion factor
u10 = wind_speed*pylab.sin(pylab.deg2rad(wind_dir))
v10 = wind_speed*pylab.cos(pylab.deg2rad(wind_dir))


fig, (mapP, mapT) = plt.subplots(1, 2)
mapP = Basemap(llcrnrlon=-10.,llcrnrlat=32,urcrnrlon=40,urcrnrlat=64,resolution=None,projection='tmerc',lon_0=10,lat_0=55, ax = mapP)
mapT = Basemap(llcrnrlon=-10.,llcrnrlat=32,urcrnrlon=40,urcrnrlat=64,resolution=None,projection='tmerc',lon_0=10,lat_0=55, ax = mapT)

mapP.shadedrelief()
mapT.shadedrelief()

plt.suptitle('Plot at %d hPa - winds are in km/h' % Pressure_level)

mapP.drawmeridians(numpy.arange(0,360,10), labels=[0,0,0,1], fontsize=10)
mapP.drawparallels(numpy.arange(-90,90,10), labels=[1,0,0,0], fontsize=10)
mapT.drawmeridians(numpy.arange(0,360,10), labels=[0,0,0,1], fontsize=10)
mapT.drawparallels(numpy.arange(-90,90,10), labels=[1,0,0,0], fontsize=10)


x,y = map((stat_height.T)[0], (stat_height.T)[1])
PressurePlot  = mapP.scatter(x, y, c = geop_height, marker='o', cmap="bwr", edgecolor = '#333333', vmin = min(geop_height), vmax = max(geop_height))
CPressurePlot = mapP.colorbar(PressurePlot, location="bottom", pad='5%', use_gridspec = True)
CPressurePlot.set_label('Height [km]')

x,y = map((stat_wind.T)[0], (stat_wind.T)[1])
WindPlot = mapP.barbs(x, y, u10, v10, pivot='tip', barbcolor='#333333', length=6)

x,y = map((stat_drtemp.T)[0], (stat_drtemp.T)[1])
dryTPlot  = mapT.scatter(x+26000,y, c = dryT, marker='s', cmap="coolwarm", edgecolor = '#333333', vmin = min(dewT), vmax = max(dryT))
x,y = map((stat_wetemp.T)[0], (stat_wetemp.T)[1])
dewTPlot  = mapT.scatter(x-26000,y, c = dewT, marker='s', cmap="coolwarm", edgecolor = '#333333', vmin = min(dewT), vmax = max(dryT))
CdryTPlot = mapT.colorbar(dryTPlot, location="bottom", pad='5%', use_gridspec = True)
CdryTPlot.set_label('T [Celsius] - (Wet bulb <- -> Dry bulb)')


plt.tight_layout(rect = [0.05, 0., 1., 1.])
fig.show()
