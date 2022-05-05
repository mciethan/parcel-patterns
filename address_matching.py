import pandas as pd

# specify files to run and city name here
files_to_run = ['joined_centroids_2016.csv']
area_name = 'Providence'
# for yr in range(2002, 2022):
#     files_to_run.append('tax_rolls/' + str(yr) + "_Property_Tax_Roll.csv")

# names of relevant input columns
parc_add = 'P_ADDR'
own_add = 'O_ADDR'
own_city = 'O_CITY'
own_st = 'O_STATE'
tract_name = 'NAMELSAD'
propid = 'PROPID'

# other global variables and constants
cols = [parc_add, own_add, own_city, own_st, tract_name, propid]
summary_table = [['file_name', 'num_parcels', 'matches', 'fuzzy', 'blanks',
                  'po_box', 'out_of_area', 'unmatched_prov']]
ABBRS = {'ST': 'STREET', 'AVE': 'AVENUE', 'RD': 'ROAD', 'PL': 'PLACE',
         'DR': 'DRIVE', 'BLVD': 'BOULEVARD', 'CT': 'COURT', 'PKWY': 'PARKWAY',
         'LN': 'LANE', 'SQ': 'SQUARE', 'TER': 'TERRACE', 'CIR': 'CIRCLE',
         'HL': 'HILL', 'PKY': 'PARKWAY', 'TR': 'TERRACE',
         'STREETSTE': 'STREET'}
UNIT_ABBRS = ['UNIT', 'BLDG', 'STE', 'FL']
ORDINALS = {'1ST': 'FIRST', '2ND': 'SECOND', '3RD': 'THIRD', '4TH': 'FOURTH',
            '5TH': 'FIFTH', '6TH': 'SIXTH', '7TH': 'SEVENTH', '8TH': 'EIGHTH',
            '9TH': 'NINTH', '10TH': 'TENTH', '11TH': 'ELEVENTH', '12TH':
                'TWELFTH'}


def num_from_string(str_with_digits):
    """
    Extracts and returns the numerical elements of a string containing digits.
    """
    to_num = ""
    for char in str_with_digits:
        if char.isdigit():
            to_num += char
    return int(to_num)


def get_range(num, interval: int) -> list:
    """
    Given an object num, which could be a number or could be some string with
    numeric elements in it, return a list representing a range of numbers 
    containing num, going up and down by some given interval.  For example, a
    num of 12 and an interval of 5 would return [7, 12, 19]
    """
    rng = None

    if num.isnumeric():
        rng = [int(num) - interval, int(num), int(num) + interval]
    elif '-' in num:  # handles things like 12-15 main st
        f, t = num.split('-', 1)
        f_range = get_range(f, interval)
        t_range = get_range(t, interval)
        if f_range is not None:
            return f_range
        else:
            return t_range
    elif any(char.isdigit() for char in num):  # handles things like 12A main st
        n = num_from_string(num)
        rng = [int(n) - interval, int(n), int(n) + interval]

    return rng


def fuzzy_match(addr_dict, addr):
    """
    Checks if a given address is numerically close to an address listed in the
    address dictionary.  Returns the matching address if so, False otherwise.
    """
    if ' ' not in addr:
        return False
    num, rst = addr.split(None, 1)
    interval = 100  # the choice of interval is somewhat arbitrary, for now
    addr_number_range = get_range(num, interval)
    if addr_number_range is None:  # if 1st element of address is not numeric
        return False

    # these variables are the bounds and middle of the range to search
    fr = addr_number_range[0]
    middle_of_range = addr_number_range[1]
    to = addr_number_range[2]

    # these variables will act as counters in the while loop
    up_num = middle_of_range
    down_num = middle_of_range

    # if 95 main st is the address, this loop checks if 96 main st and 94 main 
    # st are in address_dict, then 97 main st and 93 main st, etc.
    while up_num <= to or down_num >= fr:
        up_num += 1
        down_num -= 1
        if str(up_num) + ' ' + rst in addr_dict:
            return str(up_num) + ' ' + rst
        elif str(down_num) + ' ' + rst in addr_dict:
            return str(down_num) + ' ' + rst

    return False


def fuzzy_area_match(area_1: str, area_2: str) -> bool:
    """
    Given two area names, returns True if the first 6 characters match and
    False otherwise.  This is a functional but not-ideal way to handle the
    misspellings of city names that sometimes crop up in parcel datasets.
    """
    if len(area_1) >= 6 and len(area_2) >= 6:
        return area_1[:6] == area_2[:6]
    else:
        return area_1 == area_2


def variation(f: str, r: str, lookup: dict):
    """
    Returns an address string where the last word has been replaced by something
    else.  For example, 12 Main St would be replaced by 12 Main Street using the
    ABBRS dictionary, and 24 5th Ave would be replaced by 24 Fifth Ave using the
    ORDINALS dictionary.  This method is mainly used for readability.  
    """
    return f + " " + lookup[r]


def record(addr: str, addr_dict: dict, prop_id):
    """
    Adds a given address to the given address dictionary, with the given parcel
    ID as the value.  This method is mainly used for readability.
    """
    addr_dict[addr] = prop_id


def record_street_variations(fst: str, rst: str, addr_dict: dict, prop_id):
    """
    For an address where the last word is a street abbreviation, adds variations
    to the address dictionary. Specifically, ordinal street names are replaced
    with their written-out versions, and both the address with the street 
    abbreviation and the address without it (i.e. "12 Main St" and "12 Main") 
    are added to the address dictionary.
    """
    if ' ' in fst:
        fs, rs = fst.rsplit(None, 1)
        if rs in ORDINALS:  # replace "2ND" with "SECOND", etc.
            fst = variation(fs, rs, ORDINALS)
    record(variation(fst, rst, ABBRS), addr_dict, prop_id)
    record(fst, addr_dict, prop_id)


def record_variations(addr: str, addr_dict: dict, prop_id):
    """
    Adds variations of an address to the address dictionary by stripping words
    from the end of the address string, checking for common street-type or
    apartment-unit abbreviations, and adding versions of the address with and
    without those abbreviations into the address dictionary.
    """
    if ' ' in addr:
        fst, rst = addr.rsplit(None, 1)  # last word of address

        if rst in ABBRS:  # if the last word is something like ST, RD, DR, etc.
            record_street_variations(fst, rst, addr_dict, prop_id)

        # this part deals with addresses that end in a unit number
        elif len(rst) == 1 or any(char.isdigit() for char in rst):
            fs, rs = fst.rsplit(None, 1)

            if rs in UNIT_ABBRS:
                f, r = fs.rsplit(None, 1)
                if r in ABBRS:  # i.e. 12 main st unit 5A
                    record_street_variations(f, r, addr_dict, prop_id)
                else:  # i.e. 12 main unit 5A
                    record(fs, addr_dict, prop_id)
            elif rs in ABBRS:  # i.e. 12 main st 5A
                record_street_variations(fs, rs, addr_dict, prop_id)
            else:  # i.e. 12 main 5A
                record(fs, addr_dict, prop_id)


def add_alternate(addr: str, alternates: dict, prop_id):
    """
    Adds a given address to a given dictionary of alternate addresses, either by
    initializing a new list of alternates (if the property ID is not already in
    the alternates dictionary) or by appending the address to an existing list.
    """
    if prop_id not in alternates:
        alternates[prop_id] = [addr]
    else:
        alternates[prop_id].append(addr)


def add_street_alternates(fst: str, rst: str, alternates: dict, prop_id):
    """
    For an address where the last word is a street abbreviation, adds variations
    to the alternates list for the given property ID. Specifically, ordinal 
    street names are replaced with their written-out versions, and versions of 
    the address with and without the street abbreviation (i.e. "12 Main St" and 
    "12 Main") are added to the list of alternates.
    """
    if ' ' in fst:
        fs, rs = fst.rsplit(None, 1)
        if rs in ORDINALS:  # replace "2ND" with "SECOND", etc.
            fst = fs + ' ' + ORDINALS[rs]
    add_alternate(variation(fst, rst, ABBRS), alternates, prop_id)
    add_alternate(fst, alternates, prop_id)


def populate_alternates(owner_addr: str, alternates: dict, prop_id):
    """
    Populates a list of alternate addresses for each owner address by stripping 
    words from the end of the address string, checking for common street-type or
    apartment-unit abbreviations, and adding versions of the address with and
    without those abbreviations into the alternates list.  These alternates
    lists are stored in a dictionary keyed on property IDs.
    """
    if ' ' in owner_addr:
        fst, rst = owner_addr.rsplit(None, 1)
        if rst in ABBRS:  # if the last word is something like ST, RD, DR, etc.
            add_street_alternates(fst, rst, alternates, prop_id)

        elif len(rst) == 1 or any(char.isdigit() for char in rst):  # unit nums
            if ' ' in fst:
                fs, rs = fst.rsplit(None, 1)
                if rs in UNIT_ABBRS:
                    f, r = fs.rsplit(None, 1)
                    if r in ABBRS: # i.e. 12 main st unit 5A
                        add_street_alternates(f, r, alternates, prop_id)
                        add_alternate(f + ' ' + ABBRS[r] + rs + ' ' + rst,
                                      alternates, prop_id)
                elif rs in ABBRS:
                    add_street_alternates(fs, rs, alternates, prop_id)
                    add_alternate(fs + ' ' + ABBRS[rs] + ' ' + rst,
                                  alternates, prop_id)


def get_match(addr_dict: dict, alternates: dict, prop_id):
    """
    This method is called when a listed owner address does not match any of the
    listed addresses in the address dictionary.  It scans through the list of 
    alternate versions for that address and checks to see if they are in the 
    address dictionary, or if there is a fuzzy match (an address with a nearby
    street number).  Returns the property ID and the mode (exact or fuzzy) of 
    the match if there is a match, and False otherwise.
    """
    if prop_id not in alternates:
        return False, False
    alternate_addrs = alternates[prop_id]
    for ad in alternate_addrs:
        if ad in addr_dict:
            return addr_dict[ad], "exact"
    for ad in alternate_addrs:
        fuzzy_addr = fuzzy_match(addr_dict, ad)
        if fuzzy_addr:
            return addr_dict[fuzzy_addr], "fuzzy"
    return False, False


def match_addresses(file_name: str, area_name: str) -> list:
    """
    Reads in a csv table of parcel data and categorizes each parcel as either
    owner-occupied, owned within a given area, owned outside that area, owned by
    someone using a PO Box, missing owner information, or couldn't find the 
    owner address.  Writes the parcel data with these categories to a csv, and
    returns a list with information that summarizes how many parcels fell into
    each category for the given file of parcel data.
    """
    # names of relevant output columns
    owner_occd = 'oo'
    owned_in_area = 'ia'
    owned_out_area = 'oa'
    owned_po_box = 'po'
    owner_no_info = 'xi'
    owner_not_found = 'xf'

    # reads in selected columns, fills null values, upper-cases everything
    prov = pd.read_csv(file_name)[cols].fillna('').applymap(lambda s: s.upper())

    # initialize some blank columns for keeping track of things
    prov['OWNER_AREA'] = ''
    prov[[owner_occd, owned_in_area, owned_out_area, owned_po_box,
          owner_no_info, owner_not_found]] = 0

    # adds all the parcel addresses "as they are" to the address dictionary
    # alternate versions of each parcel address will be added momentarily
    address_dict = dict(zip(prov[parc_add], prov[propid]))

    # will have lists of alternate owner address versions to check
    alternate_addresses = {}

    # keyed on property IDs, contains info like tract name and other attributes
    prop_info = {}

    # loops through the rows of the table and cleans data to get more matches
    for i in range(len(prov[parc_add])):
        ad = prov.at[i, parc_add]

        # define what info gets stores in prop_info (currently just tract name)
        prop_info[prov.at[i, propid]] = prov.at[i, tract_name]

        # add variations of the parcel address to the address dictionary
        record_variations(ad, address_dict, prov.at[i, propid])

        # add variations of the owner addresses to the alternates dictionary
        populate_alternates(prov.at[i, own_add], alternate_addresses,
                            prov.at[i, propid])

    matches = 0
    blanks = 0
    unmatched_prov = 0
    unmatched_else = 0
    fuzzy_matches = 0
    po_box = 0
    for i in range(len(prov[own_add])):
        add = prov.at[i, own_add]
        pid = prov.at[i, propid]
        if add == '':  # blanks
            blanks += 1
            prov.at[i, owner_no_info] = 1
        elif " BOX " in add:  # PO Boxes
            po_box += 1
            prov.at[i, owned_po_box] = 1
        elif not fuzzy_area_match(prov.at[i, own_city], area_name.upper()):
            unmatched_else += 1  # address not in area
            prov.at[i, owned_out_area] = 1
        else:  # address is in area
            match_id, mode = get_match(address_dict, alternate_addresses, pid)
            if mode == 'exact':
                matches += 1
                if match_id == pid:  # address prop ID equal to owner prop ID
                    prov.at[i, owner_occd] = 1
                else:
                    prov.at[i, owned_in_area] = 1
                    prov.at[i, 'OWNER_AREA'] = prop_info[match_id]
            elif mode == 'fuzzy':
                fuzzy_matches += 1
                prov.at[i, owned_in_area] = 1
                prov.at[i, 'OWNER_AREA'] = prop_info[match_id]
            else:  # no match
                unmatched_prov += 1
                prov.at[i, owner_not_found] = 1

    prov.to_csv('yearly_out/' + file_name + '_matched.csv', index=False)
    return [file_name, len(prov), matches, fuzzy_matches, blanks, po_box,
            unmatched_else, unmatched_prov]


# ------------------- READY TO RUMBLE ------------------------
for file in files_to_run:
    print("Processing " + file + "...")
    summary_table.append(match_addresses(file, area_name))
print("Success!")
pd.DataFrame(summary_table).to_csv('summary.csv', header=False, index=False)
