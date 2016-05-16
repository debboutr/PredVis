# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:04:41 2016

@author: Rdebbout
"""

from osgeo import gdal  
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *  
  
fileName = "C:\\Users\\Rdebbout\\temp\\NHDPlusV21\\NHDPlusSR\\NHDPlus09\\NHDPlusCatchment\\cat"  
bandNum1 = 1 
fileName2 =  "D:\\Projects\\RpBuf100\\RipBuf100_09.tif"
bandNum2 =  1
  
outFile = "out.tif"  
  
#Open the dataset  
ds1 = gdal.Open(fileName, GA_ReadOnly )  
band1 = ds1.GetRasterBand(bandNum1)
ds2 = gdal.Open(fileName2, GA_ReadOnly )
band2 = ds1.GetRasterBand(bandNum2)  
  
#Read the data into numpy arrays  
data1 = BandReadAsArray(band1)  
data2 = BandReadAsArray(band2)  
  
#The actual calculation  
dataOut = data1*data2
  
#Write the out file  
driver = gdal.GetDriverByName("GTiff")  
dsOut = driver.Create(outFile, ds1.RasterXSize, ds1.RasterYSize, 1, band1.DataType)  
CopyDatasetInfo(ds1,dsOut)  
bandOut=dsOut.GetRasterBand(1)  
BandWriteArray(bandOut, dataOut)  
  
#Close the datasets  
band1 = None  
band2 = None  
ds1 = None  
bandOut = None  
dsOut = None  
data1 = None
data2 = None
