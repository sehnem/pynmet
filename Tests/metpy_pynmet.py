import cartopy
import cartopy.crs as ccrs
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
import numpy as np
import pynmet

from metpy.gridding.gridding_functions import (interpolate, remove_nan_observations,
                                               remove_repeat_coordinates)

def basic_map(proj):
    """Make our basic default map for plotting"""
    fig = plt.figure(figsize=(15, 10))
    view = fig.add_axes([0, 0, 1, 1], projection=proj)
    view.set_extent([-76, -34, -37, 7])
    view.add_feature(cartopy.feature.NaturalEarthFeature(category='cultural',
                                                         name='admin_1_states_provinces_lakes',
                                                         scale='50m', facecolor='none'))
    view.add_feature(cartopy.feature.OCEAN)
    view.add_feature(cartopy.feature.COASTLINE)
    view.add_feature(cartopy.feature.BORDERS, linestyle=':')
    return view


def station_test_data(variable, codes, date, resample):
    value = []
    lat = []
    lon = []
    for code in codes:
        est = pynmet.inmet(code, local=True)
        try:
            est.resample(resample)
            value.append(est.dados[variable][date].values[0])
        except:
            continue
        lat.append(est.lat)
        lon.append(est.lon)
    return lon, lat, value




#levels = list(range(-20, 20, 1))
cmap = plt.get_cmap('Blues')
#norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

sites = pynmet.inmet.sites.index
#sites = ['A803']

lon, lat, temp = station_test_data('Precipitacao', sites, '2017-01', 'm')
lon = np.array(lon)
lat = np.array(lat)
temp = np.array(temp)


from_proj = ccrs.Geodetic()
#to_proj = ccrs.AlbersEqualArea(central_longitude=-97.0000, central_latitude=38.0000)
to_proj = ccrs.Robinson()


proj_points = to_proj.transform_points(from_proj, lon, lat)
x, y = proj_points[:, 0], proj_points[:, 1]



x, y, temp = remove_nan_observations(x, y, temp)
x, y, temp = remove_repeat_coordinates(x, y, temp)



gx, gy, img = interpolate(x, y, temp, interp_type='cressman',
                          minimum_neighbors=1, search_radius=600000, hres=25000)
img = np.ma.masked_where(np.isnan(img), img)
view = basic_map(to_proj)
mmb = view.pcolormesh(gx, gy, img, cmap=cmap)
plt.colorbar(mmb, shrink=.4, pad=0)