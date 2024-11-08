# EuroOil_bez_bio
Stáhne a v mapě zobrazí čerpací stanice EuroOil s biosložkou pod 1 procento u benzinu 95 a nafty. 

Používá shodná veřejná data jako aplikace EuroOil Srdcovka.

Potřebné pzthon balíčky nainstaluje **install_packages.py**, testováno s Python 3.12.6 na Windows.

Pro běh jsou třeba podkladova mapova data EU z adresy https://www.mapsforeurope.org/access-data, kde se zaškrtne Download u EuroGlobalMap,  I agree to the licence terms* a vyplní email. Na email přijde odkaz na stažení souboru. Ze ZIP soubor je vhodné extrahovat soubor EuroGlobalMap_2024.gpkg případně odkomentovat řádek začínající map_file = "zip://euro-global-map-g..." kdy se čte přímo ZIP archiv, ale je to výrazně pomalejší.

Příklad mapy pro benzin. Větší červená kolečka - čerpací stanice u skladů.
![stanice_kvalita_ben_nula_20241108](https://github.com/user-attachments/assets/4ad9f5db-9dbc-43c1-a040-a5914d15c0f0)
