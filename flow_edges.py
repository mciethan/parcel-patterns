import pandas as pd

# read in a csv file of parcels that are spatially joined to the names of the
# tracts or areas that contain them, and also categorized by ownership
wmr = pd.read_csv('wide_matches_2016.csv')
# print(wmr.NAMELSAD.unique())

# names of relevant columns
parcel_tract = 'NAMELSAD'
ownr_tract = 'OWNER_AREA'

# list of the unique tract or area names that contain the parcels
uniq_tracts = wmr[parcel_tract].unique()
num_tracts = len(uniq_tracts)

# dictionaries to look up tract names by index number and vice versa
t_index = {}
t_name = {}
for idx, name in enumerate(uniq_tracts):
    t_index[name] = idx
    t_name[idx] = name

# this NxN array (N = number of unique tract or area names) will be used to keep
# count of the number of parcels in one area owned in every other area
ownership_array = [[0 for c in range(num_tracts)] for r in range(num_tracts)]

for row in range(len(wmr)):
    this_tract = wmr.at[row, parcel_tract]
    owner_tract = wmr.at[row, ownr_tract]
    if this_tract in t_index and owner_tract in t_index:
        ownership_array[t_index[this_tract]][t_index[owner_tract]] += 1

# convert the NxN array of counts into a table where each row has three entries:
# the name of some tract/area A, the name of some tract/area B (could be the
# same name as tract/area A), and the count of parcels in tract/area A that are
# owned in tract/area B.  This table is written to a csv that can then be used
# to generate and symbolize a polylines feature class of flow map arrows
out_list = []
for r in range(num_tracts):
    for c in range(num_tracts):
        out_list.append([t_name[r], t_name[c], ownership_array[r][c]])
out_df = pd.DataFrame(out_list, columns=['parcel_tract', 'owner_tract', 'count'])
out_df.dropna().to_csv('flow_edges_2016.csv', index=False)
