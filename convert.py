#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import pyproj
from pykml import parser
import sys
import sqlite3

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

sotaformat = u'{"geometry":{"x":%s,"y":%s,"spatialReference":{"wkid":102100}},"symbol":{"color":[255,0,0,255],"size":7.5,"angle":0,"xoffset":0,"yoffset":0,"type":"esriSMS","outline":{"color":[255,0,0,255],"width":0.75,"type":"esriSLS","style":"esriSLSSolid"}},"identify_funcType":"MEMO_POINT_2"},{"geometry":{"x":%s,"y":%s,"spatialReference":{"wkid":102100}},"symbol":{"color":[0,0,0,255],"type":"esriTS","haloSize":1.5,"haloColor":[255,255,255,255],"horizontalAlignment":"left","angle":0,"xoffset":-27,"yoffset":-15,"text":"%s","rotated":false,"kerning":true,"font":{"size":9,"style":"normal","variant":"normal","weight":"normal","family":"ＭＳ ゴシック"}},"identify_funcType":"MEMO_POINT_2_LABEL"}'

potaformat = u'{"geometry":{"x":%s,"y":%s,"spatialReference":{"wkid":102100}},"symbol":{"color":[255,0,0,255],"type":"esriTS","haloSize":1.5,"haloColor":[255,255,255,255],"horizontalAlignment":"center","angle":0,"xoffset":0,"yoffset":-3.75,"text":"%s","rotated":false,"kerning":true,"font":{"size":12,"style":"normal","variant":"normal","weight":"bold","family":"ＭＳ ゴシック"}},"identify_funcType":"TEXT_TEXT_1"}'
            
EPSG4612 = pyproj.Proj("+init=EPSG:4612")
EPSG3857 = pyproj.Proj("+init=EPSG:3857")

argc = len(sys.argv)

if (argc < 2):
    print('Usage command kml-file sqlitedb-file')
    sys.exit(1)
elif (argc == 2):
    kml_file = sys.argv[1]
    summit_db=''
else:
    kml_file = sys.argv[1]
    summit_db= sys.argv[2]

print('[')

with open(kml_file) as f:
    root = parser.parse(f).getroot()
    for pm in root.Document.Folder.Placemark:
        name = pm.name + pm.ExtendedData.Data[0].value
        lat = pm.ExtendedData.Data[3].value
        lon = pm.ExtendedData.Data[4].value
        x,y = pyproj.transform(EPSG4612, EPSG3857, lon,lat)
        print(potaformat % (str(x), str(y),  name))
        print(',')

if (summit_db != ''):
    conn_summit = sqlite3.connect(summit_db)
    cur_summit = conn_summit.cursor()
    for s in cur_summit.execute('select * from ja_summits'):
        (code,lat,lon,pt,alt,_,_,name,_) = s
        x,y = pyproj.transform(EPSG4612, EPSG3857, lon,lat)
        print(sotaformat % (str(x), str(y), str(x), str(y),code + ' ' +name))
        print(',')
    
print('[]]')
    
