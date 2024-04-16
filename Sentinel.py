import os
import sys
import geopandas as gpd

#from source.sentinel_2_band_downloader import Sentinel2_Band_Downloader
from sentinelsat import SentinelAPI
from datetime import datetime, timedelta
from config import settings
from shapely.wkt import dumps




class sentinel_Acquisition():
    def __init__(self):
        pass

    def read_file(self, path):
        # Read shp file and return geodataframe with geometry
        gdf = gpd.read_file(path)

        return_list = []
        for index, row in gdf.iterrows():
            return_list.append(dumps(row.geometry))

        return return_list[0]
    
    def download_sentinel_files(self, roi = 'database/ROI.shp', output_path = 'data/sentinel'):
        # Download sentinel images
        #downloader = Sentinel2_Band_Downloader(output_path)
        
        api = SentinelAPI(settings.SENTINEL.user, settings.sec.copernicus.password, 'https://scihub.copernicus.eu/apihub')
       
        polygon = self.read_file(roi)
        
        start_date = datetime.utcnow() - timedelta(days=2)
        end_date = datetime.utcnow()
        cloud_cover = "100"
        type = "L2A"
        plataform_name = "SENTINEL-2"
        
        products = api.query(polygon, date = (start_date, end_date), platformname = plataform_name, cloudcoverpercentage = (0, cloud_cover), producttype = type)
        
        products_df = api.to_dataframe(products)


sentinel = sentinel_Acquisition()

file_list = sentinel.read_file('database/ROI.shp')
product = sentinel.download_sentinel_files()