import geopandas as gpd
import pandas as pd
import os

attrs_file = 'data/parcel_attributes/Boston_Property_Assessment_2021.csv'
geoms_path = 'data/parcel_geometries/Boston_Parcels_2021.geojson'

gdf = gpd.read_file(geoms_path)
num_records_before = len(gdf)

attrs_df = pd.read_csv(attrs_file, usecols=['PID', 'ST_NAME'], dtype=str)
attrs_df = attrs_df.rename(columns={"PID": "MAP_PAR_ID"})

gdf = gdf.merge(attrs_df, on='MAP_PAR_ID')
num_records_after = len(gdf)

print("Of the " + str(num_records_before) + " records in the geometry file, "
    + str(num_records_after) + " were successfully joined to parcel attributes (" 
    + str(round(num_records_after*100/num_records_before, 1)) + "%).")