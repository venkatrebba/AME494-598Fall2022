"""
Author: Venkatarao Rebba <rebba498@gmail.com>
This class intends to upload an image to Google Cloud Storage
"""
import cv2
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
import json

class CloundFunctionHandler:
    def __init__(self, credential_json) -> None:
        
        self.project_name = "myproject"
        self.bucket_name = "sai_dev_bucket"
        with open(credential_json) as json_file:
            self.gcloudCredDict = json.load(json_file)
        
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            self.gcloudCredDict
        )

        self.client = storage.Client(credentials=self.credentials, project=self.project_name)
        self.bucket = self.client.get_bucket(self.bucket_name)

    def upload_file(self, filePath):
        blob = self.bucket.blob(filePath)
        blob.upload_from_filename(filePath)
