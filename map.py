from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy

from path_variables import *
# closes previously opened plot.
plt.close()

## INSERT DATA BELOW
year  = '17'
month = '11'
day   = '10'
hour  = '00' #either 12 or 00
## INSERT DATA ABOVE

folder_path = soundings_folder + str(day)+str(month)+str(year)+'-'+str(hour)+'\\'

# loads available stations' datasets from folder
stations_filename  = 'availables.txt'
availstations_path = folder_path + stations_filename

lat, lon, IDs = numpy.loadtxt(availstations_path, unpack=True)


## INSERT DATA BELOW
# standard levels should be available for all stations. Other levels are rounded to +- 5 hPa. (for some stations this does not work).
Pressure_level = 1000.0
## INSERT DATA ABOVE

# geop_height saves the height for the given pressure. stat_height allows datasets with missing values to be plotted.
geop_height = numpy.empty(len(IDs));   stat_height = numpy.empty([len(IDs),2])
# wind_dir and wind_speed save the wind related informations. stat_wind works as before.
wind_dir    = numpy.empty(len(IDs));   stat_wind   = numpy.empty([len(IDs),2])
wind_speed  = numpy.empty(len(IDs))
# dryT and dewT represent the dry bulb and wet bulb temperatures, with stat_* working as before.
dryT        = numpy.empty(len(IDs));   stat_drtemp = numpy.empty([len(IDs),2])
dewT        = numpy.empty(len(IDs));   stat_wetemp = numpy.empty([len(IDs),2])

i = 0
deleted_h = 0; deleted_w = 0; deleted_dT = 0; deleted_wT = 0;
for stn in IDs:
	# IDs is an array of integers, so zeros at beginning of ID are deleted. This inserts them again.
    if len(str(int(stn))) < 5:
        stn = '0' + str(int(stn))
    else:
        stn = str(int(stn))

    # sounding data for stn station is loaded into a 11 dimensions array (data).
    Sounding_filename = stn + '.txt'
    data_path = folder_path + Sounding_filename

    data = numpy.array(11)
    data = numpy.loadtxt(data_path, unpack=True)

	# evaluates the array of differences between measured pressures and the given Pressure_level. actual_pressure saves the values for which difference_in_pressure is below 5 hPa, leaving then the one with the lowest difference.
	uncertainty = 5 ## UNCERTAINTY USED ON PRESSURE [hPa]
	
	difference_in_pressure = numpy.absolute(data[0] - Pressure_level)
	actual_pressure = data[0][difference_in_pressure <= uncertainty]
	difference_in_pressure = difference_in_pressure[difference_in_pressure <= uncertainty]
	if (len(actual_pressure) > 1):
	    actual_pressure = actual_pressure[difference_in_pressure == min(difference_in_pressure)]
    # in case some points differ for the same amount and program couldn't decide which one to select. The highest is taken so that the relative difference in height (should) be smaller.
    if (len(actual_pressure) > 1):
        actual_pressure = max(actual_pressure)

    # stat_* arrays are filled with lon, lat data.
    stat_height[i-deleted_h][0]  = lon[i];     stat_height[i-deleted_h][1]  = lat[i]
    stat_wind[i-deleted_w][0]    = lon[i];     stat_wind[i-deleted_w][1]    = lat[i]
    stat_drtemp[i-deleted_dT][0] = lon[i];     stat_drtemp[i-deleted_dT][1] = lat[i]
    stat_wetemp[i-deleted_wT][0] = lon[i];     stat_wetemp[i-deleted_wT][1] = lat[i]

    # missing values are deleted from corresponding array.
    # height is missing.
    if (data[1][data[0] == actual_pressure] < -1000):
        geop_height    = numpy.delete(geop_height, i-deleted_h)
        stat_height    = numpy.delete(stat_height, i-deleted_h, 0)
        deleted_h += 1
    else:
        geop_height[i-deleted_h] = data[1][data[0]==actual_pressure]
        stat_height[i-deleted_h] = numpy.array([lon[i], lat[i]])

    # wind data are missing.
    if (data[6][data[0]==actual_pressure] < -1000 or data[7][data[0]==actual_pressure] < -1000):
        wind_dir       = numpy.delete(wind_dir, i-deleted_w)
        wind_speed     = numpy.delete(wind_speed, i-deleted_w)
        stat_wind      = numpy.delete(stat_wind, i-deleted_w, 0)
        deleted_w += 1
    else:
        wind_dir[i-deleted_w]    = data[6][data[0]==actual_pressure] + 180
        wind_speed[i-deleted_w]  = data[7][data[0]==actual_pressure]
        stat_wind[i-deleted_w]   = numpy.array([lon[i], lat[i]])

	# dry bulb temperature data is missing.
    if (data[2][data[0]==actual_pressure] < -1000):
        dryT           = numpy.delete(dryT, i-deleted_dT)
        stat_drtemp    = numpy.delete(stat_drtemp, i-deleted_dT, 0)
        deleted_dT += 1
    else:
        dryT[i-deleted_dT]        = data[2][data[0]==actual_pressure]
        stat_drtemp[i-deleted_dT] = numpy.array([lon[i], lat[i]])

    # wet bulb temperature data is missing.
    if (data[3][data[0]==actual_pressure] < -1000):
        dewT           = numpy.delete(dewT, i-deleted_wT)
        stat_wetemp    = numpy.delete(stat_wetemp, i-deleted_wT, 0)
        deleted_wT += 1
    else:
        dewT[i-deleted_wT]        = data[3][data[0]==actual_pressure]
        stat_wetemp[i-deleted_wT] = numpy.array([lon[i], lat[i]])
        
    i+=1

# conversions between units of measure.
geop_height /= 1000 #m to km conversion factor.
wind_speed  *= 1.85 #knots to km/h conversion factor.
# u10 and v10 are the 'horizontal' and 'vertical' components for winds.
u10 = wind_speed*numpy.sin(numpy.deg2rad(wind_dir))
v10 = wind_speed*numpy.cos(numpy.deg2rad(wind_dir))

# figure and pressure-wind and temperature plots are initializated and filled with a mercator projection.
fig, (mapP, mapT) = plt.subplots(1, 2)
mapP = Basemap(llcrnrlon=-10.,llcrnrlat=32,urcrnrlon=40,urcrnrlat=64,resolution=None,projection='tmerc',lon_0=10,lat_0=55, ax = mapP)
mapT = Basemap(llcrnrlon=-10.,llcrnrlat=32,urcrnrlon=40,urcrnrlat=64,resolution=None,projection='tmerc',lon_0=10,lat_0=55, ax = mapT)

# fills the contours with a orographic plot.
mapP.shadedrelief()
mapT.shadedrelief()

plt.suptitle('Plot at %d +- %d hPa - winds are in km/h' % (Pressure_level, uncertainty))

# draw parallel and meridians on maps.
mapP.drawmeridians(numpy.arange(0,360,10), labels=[0,0,0,1], fontsize=10)
mapP.drawparallels(numpy.arange(-90,90,10), labels=[1,0,0,0], fontsize=10)
mapT.drawmeridians(numpy.arange(0,360,10), labels=[0,0,0,1], fontsize=10)
mapT.drawparallels(numpy.arange(-90,90,10), labels=[1,0,0,0], fontsize=10)

# converts latitudes and longitudes into values useful for matplotlib.
x,y = mapP((stat_height.T)[0], (stat_height.T)[1])
# scatters data relative to pressure onto the map.
PressurePlot  = mapP.scatter(x, y, c = geop_height, marker='o', cmap="bwr", edgecolor = '#333333', vmin = min(geop_height), vmax = max(geop_height))
CPressurePlot = mapP.colorbar(PressurePlot, location="bottom", pad='5%', use_gridspec = True)
CPressurePlot.set_label('Height [km]')

# converts lats and longs as before.
x,y = mapP((stat_wind.T)[0], (stat_wind.T)[1])
# wind data are plotted with barbs.
WindPlot = mapP.barbs(x, y, u10, v10, pivot='tip', barbcolor='#333333', length=6)

# temperature data are plotted together to show the equivalent of a skew-T plot. Wet bulb temperatures are given in the left square, dry bulb on the right. Only one colorbar is shown, because both temperatures are given in the same scale. since wet bulb temperature is always lower or at most equal to dry bulb, limits for temperature are set to the lowest wet bulb temperature and the highest dry bulb one.
x,y = mapT((stat_drtemp.T)[0], (stat_drtemp.T)[1])
dryTPlot  = mapT.scatter(x+26000,y, c = dryT, marker='s', cmap="coolwarm", edgecolor = '#333333', vmin = min(dewT), vmax = max(dryT))
x,y = mapT((stat_wetemp.T)[0], (stat_wetemp.T)[1])
dewTPlot  = mapT.scatter(x-26000,y, c = dewT, marker='s', cmap="coolwarm", edgecolor = '#333333', vmin = min(dewT), vmax = max(dryT))
CdryTPlot = mapT.colorbar(dryTPlot, location="bottom", pad='5%', use_gridspec = True)
CdryTPlot.set_label('T [Celsius] - (Wet bulb <- -> Dry bulb)')

# to fit well into the window. It is recommended to watch the plot in full window mode.
plt.tight_layout(rect = [0.05, 0., 1., 1.])
fig.show()
