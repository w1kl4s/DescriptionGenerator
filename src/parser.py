import sys, os
from datetime import datetime
import json

from ed2k import generate_hash
from anidbparser import fetch_anime_data
from filewrite import dump_to_file
class HashParser:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_paths, self.filenames = self.get_file_paths()

    def get_file_paths(self):
        paths = []
        filenames_list = []
        for root, directories, filenames in os.walk(self.folder_path):
            for filename in filenames: 
                paths.append(os.path.join(root,filename))
                filenames_list.append(filename)
        return paths, filenames_list

    def parse_directory(self):
        metadata_list = []
        metadata = {}

        for count, file_path in enumerate(self.file_paths):
            print("File {} out of {}: ".format(count + 1, len(self.file_paths)) + self.filenames[count])
            metadata = generate_hash(file_path)
            metadata['filename'] = self.filenames[count]
            metadata_list.append(metadata)
        return metadata_list

def main(dir_path):
    parser = HashParser(dir_path)
    start_time = datetime.now()
    metadata_list= parser.parse_directory()
    execution_time = (datetime.now() - start_time).total_seconds()
    for i in metadata_list:
        total_speed = (i['size']/(1024*1014))/execution_time
    print("Total hashing speed: {0:.2f} MB/sec".format(total_speed))
    filedata, animedata = fetch_anime_data(metadata_list)
    if filedata == 0:
        raise SystemExit
    dump_to_file(filedata[0], animedata)