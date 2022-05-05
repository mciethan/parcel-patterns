## Property ownership patterns: an address-matching approach
#### Ethan McIntosh, May 2022

This project is an exploration of how parcel data can be used to analyze fine-grained property ownership patterns in urban settings.  I introduce a script-based address-matching workflow which categorizes parcels by their owner addresses, and show examples of how this workflow can allow for the analysis and visualization of owner occupancy rates and landlord locations at fine spatial and temporal scales.  

### Tags
Parcel, cadastral, property, ownership, homeownership, owner-occupied, housing density, gentrification, landlord, urban, address-matching, flow maps, QGIS, graphical modeler, scripting, open-source, Python

### Background and Rationale

Many studies that examine property ownership from the standpoint of population studies rely almost exclusively on census data.  However, there's usually a delay of several years between when census data is collected and when it's released, and it also has limited spatial resolution.  

My project is meant to explore the possibility of using property parcel data produced by local tax assessors (which is increasingly available in digital formats) to derive a subset of property ownership characteristics like owner occupancy rates and landlord locations that could be used in population studies research having to do with homeownership, gentrification, or other topics related to property ownership.  Parcel data is released more frequently than census data, and because data are reported at the level of individual buildings or units, it lends itself well to analyses over small and/or nonstandard geographic areas.

However, parcel data varies meaningfully in quality and detail between cities and over time.  Therefore, the question with this project is not whether parcel data can provide finer-grained data than the census for a particular snapshot in time (it can), but rather, whether we can derive information about property ownership from parcel data that can be reasonably compared over space or time, the way we are able to do with census data.  

The following workflow derives the info from address matching, not geocoding.  it's an initial attempt, rough around the edges, functional but in active development.  

### Data Inputs and Outputs

Project description - start from parcels polygons and attributes, plus tracts or neighborhood geometries, end with parcel ownership classifications (explain the 6) and related visualizations.

#### 1) joined_centroids_qgis.py

**_Instructions:_** I built this script in the QGIS graphical modeler and exported it as a Python script.  In its Python form, it can be run in the QGIS Python console, in a project where the parcels and the neighborhoods or tracts of interest have already been loaded in as polygon vector layers.  The only pre-processing I did on the parcels layer was to save a layer of only residential parcels, since that was my specific interest, but the worklow is able to be run on all parcels or any other subset of parcels.

Running the script opens up a form with drop-down menus to select input layers.  I selected the parcels layer and told the tool which columns within that layer's attributes correspond to the parcel address and the owner address.  I also selected the neighborhoods / tracts layer and identified the name of the column from that layer that I wanted to serve as a unique name or identifier for those neighborhoods / tracts.

**_Output:_** Running the script adds a new vector layer of points to the project representing the centroids of each parcel, whose attributes include whatever attributes were in the parcels originally plus an additional column listing the name of the neighborhood or tract that geographically contains each parcel centroid.  I exported the attribute table of this joined centroids layer as a .csv file and used that as the input for the step 2.

#### 2) address_matching.py

**_Instructions:_** This is a standalone Python file that I run from a local Python console with one or more .csv files of parcels saved in either the same folder as the script or a subfolder.  Currently, each time I run the script, I first specify the relative filepaths to each parcels csv file in the file_list variable.  I have also included a variable called area_name near the top of the script where the name of the city of interest can be specified.

Each parcels .csv to be processed must have at least the following columns:

| Script Variable Name | Default Column Name  | Description | Format | Examples |
| ------------- | ------------- | ------------- | ------- | ------- |
| propid | "PROPID"  | parcel/property ID  | any, but must be unique | 27983, 1612, "0001-23-456" |
| parc_add | "P_ADDR"  | parcel address | address | "12 Main St", "12 Main Unit 5A", "12-15A Main St" |
| own_add | "O_ADDR"  | owner address  | address | "12 Main St", "PO Box 1612", "12-15A Main St Bldg 2" |
| own_city | "O_CITY"  | owner address city  | city name | "Providence", "PROVIDENCE", "New York City" |
| own_st | "O_STATE"  | owner address state  | two-character US state abbreviation | "RI", "NY", "MA" |
| tract_name | "NAMELSAD"  | tract/neighborhood name  | any | "Census Tract 36.01", "Fox Point" |

Currently, I'm either editing the parcels file to have column names matching the ones listed above, or editing the script so that the column names assigned to the above variable names match whatever those columns are names in my parcels file(s).  

**_Output:_** For each input .csv of parcels that was specified, an output .csv file is generated (with the same name as the input file, plus "\_out" at the end) which has the above columns plus the following additional columns showing how each parcel was classified based on the parcel and owner addresses.  The script also writes a "summary.csv" file in which each row displays how many parcels from each input file fell into each of these categories.

| Column Name  | Format | Description |
| ------------- | ------------- | ------- |
| oo  | 0 or 1 | owner-occupied |
| ia  | 0 or 1 | owned in-area |
| oa  | 0 or 1 | owned out-of-area |
| po  | 0 or 1 | owner address is a PO Box |
| xi  | 0 or 1 | owner address blank/missing |
| xf  | 0 or 1 | owner address not found |
| OWNER_AREA  | any | the name of the tract or neighborhood containing the owner's address |

Each parcel is categorized into exactly one of those 6 classifications. OWNER_AREA is only generated for parcels classified as "ia".  

#### 3) count_parcels_in_tracts_qgis.py

**_Instructions:_** I built the count_parcels_in_tracts_qgis.py script in the QGIS graphical modeler and exported to Python, so this script should be run the QGIS Python console.  Before doing so, however, I transferred the fields from the output csv generated in step 2 into the attributes table of the parcel centroids from step 1 using a table join ("Join attributes by field value" in QGIS).  Running the script opens up a form with drop-down menus to select input layers.  I selected the joined parcel centroids layer, the name of the column corresponding with the parcel ID, and the name of the the neighborhoods / tracts layer I'm using.

**_Output:_** Running the script adds a new vector layer of neighborhoods/tracts, whose attributes include additional columns showing how many parcels of various ownership classifications are within each tract.  The names of these added columns are as follows:

| Column Name  | Format | Description |
| ------------- | ------------- | ------- |
| oo_count  | integer | number of total parcels |
| oo_sum  | integer | number of owner-occupied parcels |
| ia_sum  | integer | number of parcels owned in-area |
| oa_sum  | integer | number of parcels owned out-of-area |
| po_sum  | integer | number of PO Box owner addresses |
| xi_sum  | integer | number of blank/missing owner addresses |
| xf_sum  | integer | number of owner addresses not found |

Using these columns, I used the field calculator in QGIS to add additionl fields of interest, like % owner occupied (oo_sum/oo_count * 100) and % owned out-of-area (oa_sum/oo_count * 100).  Any of these columns can be used for choropleth maps comparing property ownership patterns across various tracts or neighborhoods.

#### 4a) flow_edges.py

**_Instructions:_** This is a standalone Python file that I ran in a local Python console.  I saved a copy of the output csv from step 2 saved in the same folder as the script, and specified the name of this csv in the read_csv expression at the top of the script.  The csv needs to have the "NAMELSAD" (tract_name) and "OWNER_AREA" columns from step 2.

**_Output:_** Running the script generates a "flow_edges.csv" file with three columns: "parcel_tract", "owner_tract", and "count", where the numbers in "count" represent how many parcels in each parcel_tract are owned by addresses in owner_tract. There is one row for every unique combination of tracts / neighborhoods, including where the parcel tract and the owner tract are the same (i.e. parcels which aren't owner occupied but whose landlords live within the same tract / neighborhood).  

#### 4b) symbolizing flow lines in QGIS

The following steps were adapted from the following blog post by Anita Graser: https://anitagraser.com/2019/05/04/flow-maps-in-qgis-no-plugins-needed/

Before I could draw flow lines between neighborhoods, I first had to generate a points layer representing their centroids, which I called "res_centroids", whose geometries are what get used as the start and end of each line.  

To generate a feature class of flow lines, I loaded the output csv from step 4a as a standalone table in a QGIS project, chose Layer -> Add Layer -> Add/Edit Virtual Layer, inserted the following SQL expression into the "Query" box, and clicked the Add button:

```
SELECT parcel_tract
  , owner_tract
  , count
  , make_line(a.geometry, b.geometry)
FROM flow_edges
JOIN res_centroids a 
  ON flow_edges.parcel_tract = a.NAMELSAD
JOIN res_centroids b 
  ON flow_edges.owner_tract = b.NAMELSAD
WHERE a.NAMELSAD != b.NAMELSAD 
  AND flow_edges.count != 0

```

This added a temporary lines layer to my QGIS project.  After saving this layer as a permanent file, I symbolized it using a Geometry Generator with the following expression:

```
make_line(
   start_point($geometry),
   centroid(
      offset_curve(
         $geometry, 
         length($geometry)/-10.0
      )
   ),
   end_point($geometry)
)
```

I also changed the geometry type from Polygon to Line, and then within the Line symbolization options, changed the "Symbol layer type" to Arrow.  Finally, I changed the arrow width, arrow width at start, head length, and head thickness to be measured in pixels and to be data-defined (by selecting "count" from the "field type" option within each paramter's menu).  

The result of this should look like a bird's nest of arrows.  To make flow maps focused on specific tracts, I simply filtered the layer of flow arrows using expressions like 

```
"owner_trac" = 'Census Tract 34'
```

or

```
"parcel_tra" = 'Census Tract 37'
```

For each arrow, the starting point represents the tract or neighborhood of the parcel addresses, the end point represents the addresses of the landlords of those parcels, and the width is proportional to how many parcels in the starting tract/neighborhood are owned in the ending tract/neighborhood.  The direction of the arrows can be thought of as the direction of some amount of rental income.

### Future Versions

I am aiming to consolidate this workflow so that all data processing is performed in a single Python script or package, using Python geospatial libraries and 
