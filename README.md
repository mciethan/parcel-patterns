## Property ownership patterns: an address-matching approach
#### Ethan McIntosh, May 2022

This project is an exploration of how parcel data can be used to analyze fine-grained property ownership patterns in urban settings.  I introduce a script-based address-matching workflow which categorizes parcels by their owner addresses, and show examples of how this workflow can allow for the analysis and visualization of owner occupancy rates and landlord locations at fine spatial and temporal scales.  

### Tags
Parcel, cadastral, property, ownership, homeownership, owner-occupied, housing density, gentrification, landlord, urban, address-matching, flow maps, QGIS, graphical modeler, scripting, open-source, Python

### Background and Rationale

Many studies that examine property ownership from the standpoint of population studies rely almost exclusively on census data.  However, there's usually a delay of several years between when census data is collected and when it's released, and it also has limited spatial resolution.  

My project is meant to explore the possibility of using property parcel data produced by local tax assessors (which is increasingly available in digital formats), deriving a subset of property ownership characteristics like owner occupancy rates and landlord locations by comparing parcel and owner addresses, and then using that derived data for population studies research having to do with homeownership, gentrification, or other topics related to property ownership.  Parcel data is released more frequently than census data, and because data are reported at the level of individual buildings or units, it lends itself well to analyses using small and/or nonstandard geographic areas.

However, parcel data is produced by local governments, meaning that the quality and detail of data varies meaningfully between cities or over time.  Therefore, the question with this project is not whether parcel data can provide finer-grained data than the census for a particular snapshot in time (it can), but rather, whether we can derive information about property ownership from parcel data that can be reasonably compared over space or time, the way we are able to do with census data.  

(under construction)

### Data Inputs and Outputs

Project description - start from parcels polygons and attributes, plus tracts or neighborhood geometries, end with parcel ownership classifications (explain the 6) and related visualizations.

At the core of this workflow is the address matching process contained in address_matching.py.  Input is a csv of parcels (either exported from a vector layer or downloaded in tabular format) with the following columns:

| Column Header  | Description | Format | Examples |
| ------------- | ------------- | ------- | ------- |
| PROPID  | parcel/property ID  | any, but must be unique | 
| P_ADDR  | parcel address | address | "12 Main St", "12 Main Unit 5A", "12-15A Main St" |
| O_ADDR  | owner address  | address | "12 Main St", "PO Box 1612", "12-15A Main St Bldg 2" |
| O_CITY  | owner address city  | city name | "Providence", "PROVIDENCE", "New York City" |
| O_STATE  | owner address state  | two-character US state abbreviation | "RI", "NY", "MA" |
| NAMELSAD  | tract/neighborhood name  | any | "Census Tract 36.01", "Fox Point" |

1) joined centroids.  built in QGIS graphical modeler, shared here as a QGIS processing script exported directly from the graphical modeler.  Input is the parcels polygon layer and the areas polygon layer, output is the parcels as a point layer with an extra attribute: the name of the area within which it's contained.  

Code descriptions of the four parts and how to run them (inputs, outputs, links between them)

Future version will do all the processing parts in Python geospatial libraries and leave QGIS for visualization.
