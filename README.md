# EuroOil_bez_bio
Stáhne a v mapě zobrazí čerpací stanice EuroOil s biosložkou pod 1 procento u benzinu 95 a nafty. 

Používá shodná veřejná data jako aplikace EuroOil Srdcovka.

Potřebné pzthon balíčky nainstaluje **install_packages.py**, testováno s Python 3.12.6 na Windows.

Součástí repozitory jsou soubory s cache (uložený obsah pracovní paměti) mapových dat pro Českou republiku. Mělo by to stačit pro běh. V případě nefunkčnosti je třeba stáhnout podkladová mapová data EU z adresy https://www.mapsforeurope.org/access-data, kde se zaškrtne Download u EuroGlobalMap,  I agree to the licence terms* a vyplní email. Na email přijde odkaz na stažení souboru. Ze ZIP souboru je vhodné extrahovat soubor EuroGlobalMap_2024.gpkg a umístit ho do stejného adresáře jako skript. Případně lze odkomentovat řádek začínající map_file = "zip://euro-global-map-g..." kdy se čte přímo ZIP archiv, ale je to výrazně pomalejší.

Příklad generované mapy. Větší červená kolečka - čerpací stanice u skladů.
![stanice_kvalita_ben_nula_20241108](https://github.com/user-attachments/assets/e217c6e0-a40c-43ab-87a9-17f2e3dea6d6)

