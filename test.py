import geopandas as gpd
import pandas as pd
import pygeos
gpd.options.use_pygeos = True
import os

attrs_file = 'data/parcel_attributes/Boston_Property_Assessment_2021.csv'
geoms_path = 'data/parcel_geometries/Boston_Parcels_2021.geojson'
tracts_path = 'data/tract_geometries/census2020_tracts.json'

gdf = gpd.read_file(geoms_path)
num_records_before = len(gdf)

attrs_df = pd.read_csv(attrs_file, usecols=['PID','ST_NUM','ST_NAME','UNIT_NUM','CITY','ZIPCODE'], dtype=str)
attrs_df = attrs_df.rename(columns={"PID": "MAP_PAR_ID"})

gdfj = gdf.merge(attrs_df, on='MAP_PAR_ID')
num_records_after = len(gdfj)

print("Of the " + str(num_records_before) + " records in the geometry file, "
    + str(num_records_after) + " were successfully joined to parcel attributes (" 
    + str(round(num_records_after*100/num_records_before, 1)) + "%).")

gdfj['centroid_geom'] = gdfj.centroid

tdf = gpd.read_file(tracts_path)
gdfcrp = gdfj.to_crs(tdf.crs)

nrb = len(gdfcrp)
gdfcrpj = gdfcrp.sjoin(tdf, how='inner', predicate='within')
nra = len(gdfcrpj)
print("Census tracts identified for " + str(nra) + " out of "
    + str(nrb) + " parcels (" + str(round(nra*100/nrb, 1)) + "%).")
