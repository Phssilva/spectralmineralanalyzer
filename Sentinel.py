import os
import sys
import geopandas as gpd

from source.sentinel_2_band_downloader import Sentinel2_Band_Downloader
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
    
    def download_scl_files(self, roi = 'database/ROI.shp', output_path = 'data/sentinel'):
        # Download sentinel images
        downloader = Sentinel2_Band_Downloader(output_path)
        
        #api = SentinelAPI(settings.SENTINEL.user, settings.SENTINEL.password)
        access_token, refresh_token, dt_access_token = downloader.connect_to_api(settings.SENTINEL.user,
                                                                                settings.sec.copernicus.password)
        
        polygon = self.read_file(roi)
        
        start_date = datetime.utcnow() - timedelta(days=30)
        end_date = datetime.utcnow()
        cloud_cover = "100"
        type = "L2A"
        plataform_name = "SENTINEL-2"
        
        filter_list = downloader.construct_query(polygon, start_date, end_date, cloud_cover, type, plataform_name)
        
        bands_dict = {"L1C":["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B10", "B11", "B12", "TCI"],
                "L2A":{"10m": ["AOT", "B02", "B03", "B04", "B08", "TCI", "WVP"],
                "20m": ["AOT","B01", "B02", "B03", "B04", "B05","B06", "B07", "B8A", "B11", "B12", "SCL", "TCI", "WVP"],
                "60m": ["AOT","B01", "B02", "B03", "B04", "B05","B06", "B07", "B8A", "B09","B11", "B12", "SCL", "TCI", "WVP"]}}
        
        #(self, access_token, params, bands_dict, 
        #                        dt_access_token, refresh_token, tile)
        product_info = downloader.download_sentinel2_bands(access_token, 
                                                        filter_list, 
                                                        bands_dict,dt_access_token,
                                                        refresh_token, 
                                                        None)
        
        return product_info
        
    

sentinel = sentinel_Acquisition()

file_list = sentinel.read_file('database/ROI.shp')
product = sentinel.download_scl_files()