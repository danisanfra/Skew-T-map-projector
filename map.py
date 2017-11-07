from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy

from path_variables import *
plt.close()

stations_filename  = 'availables.txt'
availstations_path = folder_path + stations_filename

lat, lon, IDs = numpy.loadtxt(availstations_path, unpack=True)

## INSERT DATA BELOW
year  = '17'
month = '10'
day   = '09'
hour  = '00' #either 12 or 00
## INSERT DATA ABOVE

folder_path = soundings_folder + str(day)+str(month)+str(year)+'-'+str(hour)+'\\'

## INSERT DATA BELOW
Pressure_level = 850.0
## INSERT DATA ABOVE

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

	difference_in_pressure = numpy.absolute(data[0] - Pressure_level)
	actual_pressure = data[0][difference_in_pressure <= 5]
	if (len(actual_pressure) > 1):
    	actual_pressure = actual_pressure[difference_in_pressure == min(difference_in_pressure)]
    
    stat_height[i] = lon[i], lat[i]
    stat_wind[i]   = lon[i], lat[i]
    stat_drtemp[i] = lon[i], lat[i]
    stat_wetemp[i] = lon[i], lat[i]
    
    if (data[1][data[0] == actual_pressure] == -9999.):
        geop_height    = numpy.delete(geop_height, i)
        stat_height    = numpy.delete(stat_height, i, 0)
    else:
        geop_height[i] = data[1][data[0]==actual_pressure]
    
    if (data[6][data[0]==actual_pressure] == -9999. or data[7][data[0]==actual_pressure] == -9999.):
        wind_dir       = numpy.delete(wind_dir, i)
        wind_speed     = numpy.delete(wind_speed, i)
        stat_wind      = numpy.delete(stat_wind, i, 0)
    else:
        wind_dir[i]    = data[6][data[0]==actual_pressure] + 180
        wind_speed[i]  = data[7][data[0]==actual_pressure]
        
    if (data[2][data[0]==actual_pressure] == -9999.):
        dryT           = numpy.delete(dryT, i)
        stat_drtemp    = numpy.delete(stat_drtemp, i, 0)
    else:
        dryT[i]        = data[2][data[0]==actual_pressure]
    
    if (data[3][data[0]==actual_pressure] == -9999.):
        dewT           = numpy.delete(dewT, i)
        stat_wetemp    = numpy.delete(stat_wetemp, i, 0)
    else:
        dewT[i]        = data[3][data[0]==actual_pressure]
        
    i+=1


geop_height /= 1000 #m to km conversion factor
wind_speed  *= 1.85 #knots to km/h conversion factor
u10 = wind_speed*numpy.sin(numpy.deg2rad(wind_dir))
v10 = wind_speed*numpy.cos(numpy.deg2rad(wind_dir))


fig, (mapP, mapT) = plt.subplots(1, 2)
mapP = Basemap(llcrnrlon=-10.,llcrnrlat=32,urcrnrlon=40,urcrnrlat=64,resolution=None,projection='tmerc',lon_0=10,lat_0=55, ax = mapP)
mapT = Basemap(llcrnrlon=-10.,llcrnrlat=32,urcrnrlon=40,urcrnrlat=64,resolution=None,projection='tmerc',lon_0=10,lat_0=55, ax = mapT)

mapP.shadedrelief()
mapT.shadedrelief()

plt.suptitle('Plot at %d +- 5 hPa - winds are in km/h' % Pressure_level)

mapP.drawmeridians(numpy.arange(0,360,10), labels=[0,0,0,1], fontsize=10)
mapP.drawparallels(numpy.arange(-90,90,10), labels=[1,0,0,0], fontsize=10)
mapT.drawmeridians(numpy.arange(0,360,10), labels=[0,0,0,1], fontsize=10)
mapT.drawparallels(numpy.arange(-90,90,10), labels=[1,0,0,0], fontsize=10)

x,y = mapP((stat_height.T)[0], (stat_height.T)[1])
PressurePlot  = mapP.scatter(x, y, c = geop_height, marker='o', cmap="bwr", edgecolor = '#333333', vmin = min(geop_height), vmax = max(geop_height))
CPressurePlot = mapP.colorbar(PressurePlot, location="bottom", pad='5%', use_gridspec = True)
CPressurePlot.set_label('Height [km]')

x,y = mapP((stat_wind.T)[0], (stat_wind.T)[1])
WindPlot = mapP.barbs(x, y, u10, v10, pivot='tip', barbcolor='#333333', length=6)

x,y = mapT((stat_drtemp.T)[0], (stat_drtemp.T)[1])
dryTPlot  = mapT.scatter(x+26000,y, c = dryT, marker='s', cmap="coolwarm", edgecolor = '#333333', vmin = min(dewT), vmax = max(dryT))
x,y = mapT((stat_wetemp.T)[0], (stat_wetemp.T)[1])
dewTPlot  = mapT.scatter(x-26000,y, c = dewT, marker='s', cmap="coolwarm", edgecolor = '#333333', vmin = min(dewT), vmax = max(dryT))
CdryTPlot = mapT.colorbar(dryTPlot, location="bottom", pad='5%', use_gridspec = True)
CdryTPlot.set_label('T [Celsius] - (Wet bulb <- -> Dry bulb)')


plt.tight_layout(rect = [0.05, 0., 1., 1.])
fig.show()
