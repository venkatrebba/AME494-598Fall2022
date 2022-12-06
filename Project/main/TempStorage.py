"""
Author: Venkatarao Rebba <rebba498@gmail.com>

This is a temparary storage class that automatically deletes the records after defined timeout.

"""

import time

class TempStorage:
    def __init__(self) -> None:
        self.ExpiryTime = 60 # secs
        self.face_embedding_map = {}
        self.expiryMap = {}
    
    def getFaceNamesAndEmbeddings(self):
        self.deleteOldRecords() # Delete expired data
        data_map = [(face, embedding) for face, embedding in self.face_embedding_map.items()]
        # Returning Face Names and embeddings
        return [d[0] for d in data_map], [d[1] for d in data_map]

    def addNewFace(self, name, embedding, ts=time.time()):
        self.expiryMap[name] = ts
        self.face_embedding_map[name] = embedding

    def updateExpiryTime(self, name, ts=time.time()):
        self.expiryMap[name] = ts

    def deleteOldRecords(self):
        del_names = []
        cur_time = time.time()
        for name in self.expiryMap.keys():
            insertTs = self.expiryMap[name]
            if (cur_time - insertTs) > self.ExpiryTime:
                del_names.append(name)

        for name in del_names:
            self.expiryMap.pop(name)
            self.face_embedding_map.pop(name)