from shapely.geometry.polygon import Polygon
xlist = []
ylist = []
for index, row in selElev.iterrows():
    if type(row.geometry) == type(Polygon()):
        xls, yls = row.geometry.exterior.coords.xy
        xlist.append(xls.tolist())
        ylist.append(yls.tolist())
    else:
        poly = []
        for pol in row.geometry:
            poly.append(pol)
        for bnd in range(len(poly)):
            xls, yls = poly[bnd].exterior.coords.xy
            xlist.append(xls.tolist())
            ylist.append(yls.tolist())  