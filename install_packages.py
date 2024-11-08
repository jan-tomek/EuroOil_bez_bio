import os

packages=['requests','pandas','geopandas','matplotlib','openpyxl']

os.system('python.exe -m pip install --upgrade pip')

for p in packages:
    os.system('python.exe -m pip install ' + p)
                
                
                
                
                