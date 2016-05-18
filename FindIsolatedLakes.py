# -*- coding: utf-8 -*-
"""
Created on Fri May 06 10:30:14 2016

@author: Rdebbout
"""


import arcpy
import pandas as pd
import pysal as ps
from datetime import datetime

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
                   
# DataFrame created to link together data to dig into NHD folder structure and be iterated thru
lookup= pd.DataFrame({ 
  'hydro.rgns':["01","02","03S","03N","03W","04","05","06","07","08","09","10L","10U","11","12","13","14","15","16","17","18"],
  'rgns':["NE","MA","SA","SA","SA","GL","MS","MS","MS","MS","SR","MS","MS","MS","TX","RG","CO","CO","GB","PN","CA"]})

#--------------------------------------------------------
# !!!DIRECTORIES TO WRITE INFO TO!!!

# Shapefile or gdb feature layer to store on and off-network lakes
outfeature = 'D:/Projects/lakesAnalysis/new/NetworkLakes.shp'
outfeature2 = 'D:/Projects/lakesAnalysis/new/IsolatedLakes.shp'


# count is used when iterating to use arcpy.CopyFeatures_management() tool first pass thru
# and then arcpy.Append_management() the remaining iterations to add selected lakes to the files
count = 0
startTime = datetime.now()
for i, hr in lookup.iterrows():
    print 'on region ' + hr[1] + ' and hydro number ' + hr[0]
    # create directories to NHD data
    NHDdir = "C:/Users/Rdebbout/temp/NHDPlusV21/NHDPlus%s/NHDPlus%s"%(hr[1],hr[0])
    NHDWaterbody = "%s/NHDSnapshot/Hydrography/NHDWaterbody.shp"%(NHDdir)
    NHDWaterbodyDBF = "%s/NHDSnapshot/Hydrography/NHDWaterbody.dbf"%(NHDdir)
    NHDFlowlineDBF = "%s/NHDSnapshot/Hydrography/NHDFlowline.dbf"%(NHDdir)
    NHDPlusFlowlinVAADBF = '%s\\NHDPlusAttributes\\PlusFlowlineVAA.dbf'%(NHDdir)
    NHDCatchmentDBF = '%s\\NHDPlusCatchment\\Catchment.dbf'%(NHDdir)     
    # get waterbodies and select out by FTYPE
    arcpy.MakeFeatureLayer_management(NHDWaterbody, "NHDWaterbody", "\"FTYPE\" IN ( 'LakePond' , 'Reservoir' )")
    #arcpy.AddField_management("NHDWaterbody","VPU","TEXT")
    #arcpy.CalculateField_management("NHDWaterbody","VPU",repr(hr[0]), "PYTHON_9.3")
    #--------------------------------------------------------
    db = ps.open(NHDWaterbodyDBF)
    wb = pd.DataFrame(db[:]) 
    wb.columns = map(str.upper, db.header)
    db.close()
    wb = wb.loc[wb['FTYPE'].isin(['LakePond','Reservoir'])]
    #--------------------------------------------------------
    # get flowline table into pandas data frame 
    db = ps.open(NHDFlowlineDBF)
    fl = pd.DataFrame(db[:])
    fl.columns = map(str.upper, db.header) 
    db.close()
    #--------------------------------------------------------
    # get catchment table into pandas data frame 
    db = ps.open(NHDCatchmentDBF)
    cat = pd.DataFrame(db[:])
    cat.columns = map(str.upper, db.header)
    db.close()
    #--------------------------------------------------------
    flowcat = pd.merge(cat,fl,left_on='FEATUREID',right_on='COMID', how='inner') 
    join = pd.merge(wb,flowcat,left_on='COMID', right_on='WBAREACOMI', how='left')
    #--------------------------------------------------------
    # get NHDPlusFlowlineVAA table into pandas data frame
    db = ps.open(NHDPlusFlowlinVAADBF)
    vaa = pd.DataFrame(db[:])
    vaa.columns = map(str.upper, db.header)
    db.close()  
    #--------------------------------------------------------
    # Merge VAA table on to joined table of catchment, waterbody, and flowline tables
    joinVAA = pd.merge(join,vaa,left_on='COMID_y',right_on='COMID', how='left')
    # create data frame to link catchment COMID to waterbody COMID
    df = pd.DataFrame(columns=('catCOMID', 'wbCOMID'))
    # iterate through table while grouping by the waterbody COMID to select out associated catchments
    for name, group in joinVAA.groupby('COMID_x'):
        if not pd.isnull(group.FEATUREID).any():
            hydro = pd.Series.min(group.HYDROSEQ)
            group = group[group.HYDROSEQ == hydro]           
            s = pd.DataFrame({'catCOMID':pd.Series([int(group.COMID_y.values[0])]),'wbCOMID':pd.Series([int(group.COMID_x.values[0])])})
            df = df.append(s)
    # convert list values into integers and format to pass into SelectLayerByAttribute function 
    wblist = [int(x) for x in df.wbCOMID.tolist()]            
    offstring = '"COMID" IN (%s)'%wblist   
    whereclause = offstring.translate(None,'[]')    
    # Process: Select Layer By Attribute
    arcpy.SelectLayerByAttribute_management("NHDWaterbody", "NEW_SELECTION", whereclause)
    #add waterbodies to NetworkLakes
    if count == 0:
       arcpy.CopyFeatures_management('NHDWaterbody', outfeature)
    if count > 0:
        arcpy.Append_management("NHDWaterbody",outfeature,"NO_TEST")
    #Switch Selection
    arcpy.SelectLayerByAttribute_management("NHDWaterbody", "SWITCH_SELECTION")
    #add remaining waterbodies to IsolatedLakes 
    if count == 0:
       arcpy.CopyFeatures_management ('NHDWaterbody', outfeature2)
    if count > 0:
        arcpy.Append_management("NHDWaterbody",outfeature2,"NO_TEST")
    arcpy.Delete_management("NHDWaterbody")
    count+=1
bnd_dir = "C:/Users/Rdebbout/temp/NHDPlusV21/NHDPlusGlobalData/BoundaryUnit.shp"
    
# get waterbodies and select out by FTYPE
arcpy.MakeFeatureLayer_management(bnd_dir, "Boundaries")
arcpy.MakeFeatureLayer_management(outfeature2, "IsoLakes")

# Select the 969 waterbodies that are NOT within RPU boundaries and remove
arcpy.SelectLayerByLocation_management("IsoLakes", "COMPLETELY_WITHIN", "Boundaries", "", "NEW_SELECTION")
arcpy.SelectLayerByAttribute_management("IsoLakes", "SWITCH_SELECTION")
arcpy.DeleteFeatures_management("IsoLakes")

arcpy.Delete_management("IsoLakes")
arcpy.Delete_management("Boundaries")