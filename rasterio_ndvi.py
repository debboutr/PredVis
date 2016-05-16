"""
Created on Sun May 15 19:43:03 2016

@author: rick
"""
import rasterio, numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

with rasterio.open("RGB_NIR_Composite.tif") as image:
    print image
    blue = image.read_band(1)
    green = image.read_band(2)
    red = image.read_band(3)
    nir = image.read_band(4)
    
# Convert the red and nir bands to numpy arrays with type float for NDVI calculation
red = np.array(red, dtype=float)
nir = np.array(nir, dtype=float)

# Create variables for the NDVI formula
num = nir - red
denom = (nir + red) + 0.00000000001  # we add the 0.00000000001, so that we never divide by 0.0
# note: I tried to use seterr to ignore errors from dividing by 0.0 but it does not seem to work in this scenario

# Create a new numpy array by dividing num and denom
ndvi = np.divide(num,denom)

# Create a new numpy array to stretch NDVI values for computer display
# Note: this is a simple stretch so that you can preview the image in grayscale
stretched_ndvi = (ndvi + 1) * 255 
# BONUS: you can also use the colormap code to assign RGB colors to pixel values, instead of simply stretching the image to grayscale
# More details: https://github.com/mapbox/rasterio/blob/master/docs/colormaps.rst

# Export a new GeoTIFF of the stretched NDVI
# Note: you will get a warning that the GDAL style is changing in the updated version of Rasterio
kwargs = image.meta
kwargs.update(dtype = rasterio.uint8, count = 1, compres = 'lzw')

with rasterio.open('stretched_ndvi.tif', 'w', **kwargs) as stretchedraster:
    stretchedraster.write_band(1, stretched_ndvi.astype(rasterio.uint8))
    print 'export successful'



 
# Create a histogram function
def rasterHistogram(raster_matrix):
    '''Accepts matrix and generates histogram'''
     
    # Line above is function docstring
    # Flatten 2d-matrix
    flat_raster = ma.compressed(raster_matrix)
     
    # Setup the plot (see matplotlib.sourceforge.net)
    fig = plt.figure(figsize=(8,11))
    ax = fig.add_subplot(1,1,1)
     
    # Plot histogram
    ax.hist(flat_raster, 10, normed=0, histtype='bar',
            align='mid')
    # Show the plot on screen
    plt.show()

with rasterio.open("stretched_ndvi.tif") as image:
    print image
    blue = image.read_band(1)
# Open a raster using rasterIO
#...
# Pass matrix representation of raster to function
rasterHistogram(blue)
# Shows histogram on screen

with rasterio.open("stacked_composite.tif") as image:
    print image
    blue = image.read_band(1)
    green = image.read_band(2)
    red = image.read_band(3)
    nir = image.read_band(4)
    
    
red = np.array(red, dtype=float)
nir = np.array(nir, dtype=float)

# Create variables for the NDVI formula
num = nir - red
denom = (nir + red) + 0.00000000001

ndvi = np.divide(num,denom)

rasterHistogram(ndvi)

stretched_ndvi = (ndvi + 1) * 255 



kwargs = image.meta
kwargs.update(dtype = rasterio.uint8, count = 1, compres = 'lzw')

with rasterio.open('stretched_ndvi.tif', 'w', **kwargs) as stretchedraster:
    stretchedraster.write_band(1, stretched_ndvi.astype(rasterio.uint8))
    print 'export successful'