import pip

def install(package):
    pip.main(["show", package])

print('Requirements:')
print()

try:
    import os
except ImportError:
    install("os")
print('os - OK')

try:
    import numpy
except ImportError:
    install("numpy")
print('numpy - OK')

try:
    import matplotlib.pyplot
except ImportError:
    install("matplotlib.pyplot")
print('matplotlib.pyplot - OK')

try:
    from urllib.request import urlopen
except ImportError:
    install("urllib3")
print('urllib3 - OK')

try:
    from bs4 import BeautifulSoup
except ImportError:
    install("bs4")  
print('bs4 - OK')

try:
    from mpl_toolkits.basemap import Basemap
except ImportError:
    print('You need to download and install Pyproj [http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj]')
    print('\tRun [pip install your_package.whl] from the folder where you saved it.')
    print()
    print('You need to download and install Basemap [http://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap]')
    print('\tRun [pip install your_package.whl] from the folder where you saved it.')
print('basemap - OK')

try:
    from mpl_toolkits.basemap import Basemap
    
    map = Basemap(llcrnrlon=-10.,llcrnrlat=32,urcrnrlon=40,urcrnrlat=64,resolution=None,projection='tmerc',lon_0=10,lat_0=55)
    map.shadedrelief()
    matplotlib.pyplot.close()
except ImportError:
    print('You need to download and install Pillow from [https://pypi.python.org/pypi/Pillow/2.7.0]')
    print('\tRun [pip install your_package.whl] from the folder where you saved it.')
print('Pillow - OK')