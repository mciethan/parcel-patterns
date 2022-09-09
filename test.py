import geopandas as gpd
import os

attrs_file = 'data/parcel_attributes/Boston_Property_Assessment_2021.csv'
geoms_path = 'data/parcel_geometries/Boston_Parcels_2021.geojson'

gdf = gpd.read_file(geoms_path)
print(gdf.columns)

