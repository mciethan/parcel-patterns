## Urban property ownership patterns: an address-matching approach
#### Ethan McIntosh, May 2022

I wrote these scripts for an undergraduate project exploring how parcel data can be used to analyze fine-grained property ownership patterns in urban settings.  I developed a script-based address-matching workflow which categorizes parcels by their owner addresses, and produced examples of how this workflow can allow for the analysis and visualization of owner occupancy rates and landlord locations at fine spatial and temporal scales.  

<p align="center">
  <img src="https://github.com/mciethan/parcel-patterns/blob/main/flowmaps.png">
</p>

Read the full project paper here: https://drive.google.com/file/d/1iNafoDogle7K_C7DIjo9AOAS2rO_cbuW/view?usp=sharing

### Tags
Parcel, cadastral, property, ownership, homeownership, owner-occupied, housing density, gentrification, landlord, urban, address-matching, flow maps, QGIS, graphical modeler, scripting, open-source, Python

### How to Run this Code

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

**_Output:_** For each input .csv of parcels that was specified, an output .csv file is generated (with the same name as the input file, plus "\_out" at the end) which has the above columns plus the following additional columns showing how each parcel was classified based on the parcel and owner addresses.  The script also writes a "summary.csv" file in which each row displays how many parcels from each input file fell into each of these categories as well as the total number of parcels.  

| Column Name  | Format | Category Name | Category Meaning |
| ------------- | ------------- | ------- | ------ |
| "oo"  | 0 or 1 | owner-occupied | parcel address matches owner address |
| "ia"  | 0 or 1 | in-area | owner address is within the study area |
| "oa"  | 0 or 1 | out-of-area | owner address is outside the study area |
| "po"  | 0 or 1 | PO Box | owner address is a PO Box |
| "xi" | 0 or 1 | no info | owner address is blank or missing |
| "xf" | 0 or 1 | not found | owner address is in the study area, but couldn't be matched to a parcel address |
| "OWNER_AREA"  | any |  | the name of the tract or neighborhood containing the owner's address |
| "O_PROPID" | any |  | the parcel ID code of the owner address' parcel |

Each parcel is categorized into exactly one of those 6 classifications. OWNER_AREA is only generated for parcels classified as "ia", and O_PROPID is only generated for "oo" parcels and "ia" parcels where the match was exact rather than fuzzy. 

The numbers in the summary.csv file can be used to calculate a "match rate" ( (total - xf)/total * 100 ) showing how well the address matching algorithm did.  My initial tests using recent parcel data from Providence, RI had match rates greater than 95%, but the algorithm will undoubtedly need to be tested on older data and data from other cities before being able to achieve those kinds of match rates in a more generalized way.

#### 3) count_parcels_in_tracts_qgis.py

**_Instructions:_** I built the count_parcels_in_tracts_qgis.py script in the QGIS graphical modeler and exported to Python, so this script should be run the QGIS Python console.  Before doing so, however, I transferred the fields from the output csv generated in step 2 into the attributes table of the parcel centroids from step 1 using a table join ("Join attributes by field value" in QGIS).  Running the script opens up a form with drop-down menus to select input layers.  I selected the joined parcel centroids layer, the name of the column corresponding with the parcel ID, and the name of the the neighborhoods / tracts layer I'm using.

**_Output:_** Running the script adds a new vector layer of neighborhoods/tracts, whose attributes include additional columns showing how many parcels of various ownership classifications are within each tract.  The names of these added columns are as follows:

| Column Name  | Format | Description |
| ------------- | ------------- | ------- |
| "oo_count"  | integer | number of total parcels |
| "oo_sum" | integer | number of owner-occupied parcels |
| "ia_sum" | integer | number of parcels owned in-area |
| "oa_sum" | integer | number of parcels owned out-of-area |
| "po_sum" | integer | number of PO Box owner addresses |
| "xi_sum" | integer | number of blank/missing owner addresses |
| "xf_sum" | integer | number of owner addresses not found |

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
