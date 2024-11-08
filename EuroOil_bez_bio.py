# -*- coding: latin-1 -*-

import pandas
import matplotlib.pyplot as plt
import geopandas
import requests
import json
import string
import os
import shutil
import time
import re

PATTERN = re.compile(r"""(?P<lat_deg>\d+)°      # Latitude Degrees
                         (?:(?P<lat_min>\d+)')? # Latitude Minutes (Optional)
                         (?:(?P<lat_sec>[\d\.]+)")? # Latitude Seconds (Optional)
                         (?P<north_south>[NS])  # North or South
                         ,
                         (?P<lon_deg>\d+)°      # Longitude Degrees
                         (?:(?P<lon_min>\d+)')? # Longitude Minutes (Optional)
                         (?:(?P<lon_sec>[\d\.]+)")? # Longitude Seconds (Optional)
                         (?P<east_west>[EW])    # East or West
                      """, re.VERBOSE)
LAT_FIELDS = ("lat_deg", "lat_min", "lat_sec")
LON_FIELDS = ("lon_deg", "lon_min", "lon_sec")

def parse_dms_string(s, out_type=float):
    values = PATTERN.match(s).groupdict()
    return tuple(sum(out_type(values[field] or 0) / out_type(60 ** idx) for idx, field in enumerate(field_names)) for field_names in (LAT_FIELDS, LON_FIELDS))

if not os.path.exists("./data"): os.mkdir("./data")

# Nacte a ulozi data z verejneho API pro cerpaci stanice

response = requests.get("https://srdcovka.eurooil.cz/api/verejne/cerpaci-stanice")
print("HTTP Response code - cerpaci-stanice: "+str(response.status_code))
stanice = response.json()

with open('data/stanice.json','w') as fd:
    fd.write(json.dumps(stanice, indent=4))

stanice_df = pandas.DataFrame(columns=['cerpaciStaniceIID','nazev','ulice','obec','okres','kraj','gprsSirka','gprsDelka','produkt','ean'])
for stan in stanice["data"]:
    if stan["neaktivni"] == False:
        for prod in stan["produkty"]: 
            if prod["ean"] == "4" or prod["ean"] == "1": 
                gps = parse_dms_string(""+stan["gprsDelka"].replace(',','.').replace(' ','')+','+stan["gprsSirka"].replace(',','.').replace(' ',''))
                l = [stan["cerpaciStaniceIID"],stan["nazev"],stan["ulice"],stan["obec"],stan["okres"],stan["kraj"],gps[0],gps[1],prod["nazev"],prod["ean"]]
                stanice_df.loc[len(stanice_df)] = l
stanice_df.to_excel("data/stanice.xlsx")

# Lokace cerpacek u skladu

stanice_sklad_df = stanice_df.query('ulice.str.contains("skladu")')
stanice_sklad_df.to_excel("data/stanice_sklad.xlsx")

# Nacte a ulozi data z verejneho API pro zavazky a parametry paliva

response = requests.get("https://srdcovka.eurooil.cz/api/verejne/kvalita")
print("HTTP Response code - kvalita: "+str(response.status_code))
kvalita = response.json()

with open('data/kvalita.json','w') as fd:
    fd.write(json.dumps(kvalita, indent=4))

kvalita_df = pandas.DataFrame(columns=['cerpaciStaniceIID','ean','datumZavozu','hodnota'])
for stanpar in kvalita["data"]: 
    for val in stanpar["hodnoty"]: 
        if val["kod"] == "4-2" or val["kod"] == "1-2": 
            l = [stanpar["cerpaciStaniceIID"],stanpar["ean"],stanpar["datumZavozu"],val["hodnota"]]
            kvalita_df.loc[len(kvalita_df)] = l

# Seradi podle obsahu bioslozky

kvalita_dfs = kvalita_df.sort_values(by=['hodnota'])
kvalita_dfs.to_excel("data/kvalita.xlsx")

# Propoji stanice a udaje o palivu

stanice_kvalita_df = pandas.merge(left=stanice_df, right=kvalita_dfs, how='left', left_on=['cerpaciStaniceIID', 'ean'], right_on=['cerpaciStaniceIID', 'ean']).sort_values(by=['hodnota']).drop_duplicates()
stanice_kvalita_ben_df = stanice_kvalita_df.query("ean == '4'")
stanice_kvalita_ben_df.to_excel("data/stanice_kvalita_ben.xlsx")
stanice_kvalita_naf_df = stanice_kvalita_df.query("ean == '1'")
stanice_kvalita_naf_df.to_excel("data/stanice_kvalita_naf.xlsx")

#Vybere a ulozi s bioslozkou < 1 %

stanice_kvalita_nula_ben_df = stanice_kvalita_ben_df.query('hodnota < 1')
stanice_kvalita_nula_ben_df.to_excel("data/stanice_kvalita_ben_nula.xlsx")
stanice_kvalita_nula_naf_df = stanice_kvalita_naf_df.query('hodnota < 1')
stanice_kvalita_nula_naf_df.to_excel("data/stanice_kvalita_naf_nula.xlsx")

# Nacte mapove podklady
print("Nacitam mapove podklady.", end = "", flush=True)

map_file = "EuroGlobalMap_2024.gpkg"
# Mnohem pomalejsi, ale cte primo soubor od EU
#map_file = "zip://euro-global-map-gpkg.zip!euro-global-map-gpkg/EuroGlobalMap_2024.gpkg"

# Nacte podkladove mapy

cz_PolbndA = geopandas.read_file(map_file,layer="PolbndA",where="ICC = 'CZ'")
print(".", end = "", flush=True)
cz_LandmaskA = geopandas.read_file(map_file,layer="LandmaskA",where="ICC = 'CZ'")
print(".", end = "", flush=True)
cz_RoadL = geopandas.read_file(map_file,layer="RoadL",where="ICC = 'CZ' and (COR = 1 or RTT = 14)")
print(".", end = "", flush=True)
world = pandas.concat([cz_PolbndA,cz_LandmaskA])

print(".", flush=True)
print("Generuji mapy.", flush=True)

figb, axb = plt.subplots(figsize=(14,8))
fign, axn = plt.subplots(figsize=(14,8))
axb.set_axis_off()
axn.set_axis_off()

# Vykresli podkladove mapy

world.plot(color="lightgray", edgecolor="black",  alpha=0.5, ax = axb)
world.plot(color="lightgray", edgecolor="black",  alpha=0.5, ax = axn)
cz_RoadL.plot(color="red", edgecolor="black",  alpha=0.2, ax = axb)
cz_RoadL.plot(color="red", edgecolor="black",  alpha=0.2, ax = axn)

# Vykresli stanice u skladu

stanice_sklad_df.plot(x="gprsDelka", y="gprsSirka", kind="scatter", color="red", s=50, ax = axb)
stanice_sklad_df.plot(x="gprsDelka", y="gprsSirka", kind="scatter", color="red", s=50, ax = axn)

# Vykresli stanice s bio < 1%

stanice_kvalita_nula_ben_df.plot(x="gprsDelka", y="gprsSirka", kind="scatter", color="green", title=f"Benzin 95, bio < 1% - " + time.strftime("%d.%m.%Y"), ax = axb)
stanice_kvalita_nula_naf_df.plot(x="gprsDelka", y="gprsSirka", kind="scatter", color="black", title=f"Nafta, bio < 1% - " + time.strftime("%d.%m.%Y"), ax = axn)

# Ulozi

figb.savefig('stanice_kvalita_ben_nula.png')
fign.savefig('stanice_kvalita_naf_nula.png')

# Odkopiruje do historie

if not os.path.exists("./data/hist"): os.mkdir("./data/hist")

shutil.copy("data/stanice_kvalita_ben.xlsx", "data/hist/stanice_kvalita_ben_" + time.strftime("%Y%m%d" + ".xlsx"))
shutil.copy("data/stanice_kvalita_naf.xlsx", "data/hist/stanice_kvalita_naf_" + time.strftime("%Y%m%d" + ".xlsx"))

shutil.copy("stanice_kvalita_ben_nula.png", "data/hist/stanice_kvalita_ben_nula_" + time.strftime("%Y%m%d" + ".png"))
shutil.copy("stanice_kvalita_naf_nula.png", "data/hist/stanice_kvalita_naf_nula_" + time.strftime("%Y%m%d" + ".png"))

### Ukaze jen ty co jsou zde zakomentovane, ulozi oba ###
#plt.close(figb)
plt.close(fign)

plt.show()

print("Hotovo.", flush=True)
