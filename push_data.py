import os
import sys
import json
import pandas as pd
import pymongo
import numpy as np
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(f"MONGO_DB_URL: {MONGO_DB_URL}")

import certifi
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.db = self.client['network_security_db']
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    def csv_to_json(self, file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
if __name__ == "__main__":
    try:
        FILE_PATH = "Network_Data/phisingData.csv" # Fixed Path
        DATABASE = "ShounakTestDB"
        Collection = "NetworkData"
        
        networkobj = NetworkDataExtract()
        
        # Fixed method name call
        records = networkobj.csv_to_json(file_path=FILE_PATH) 
        
        print(f"Records converted: {len(records)}")
        
        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
        print(f"Successfully inserted {no_of_records} records.")
        
    except Exception as e:
        # It is better to use your Custom Exception here for full traceback
        raise NetworkSecurityException(e, sys)