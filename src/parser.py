import sys
import os
from datetime import datetime
import json

from ed2k import generate_hash
from anidbparser import fetch_anime_data
from filewrite import dump_to_file
from localmediainfo import file_info
from averages import average_values

class HashParser(object):

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_paths, self.filenames = self.get_file_paths()

    def get_file_paths(self):
        paths = []
        filenames_list = []
        for root, directories, filenames in os.walk(self.folder_path):
            for filename in filenames:
                paths.append(os.path.join(root, filename))
                filenames_list.append(filename)
        return paths, filenames_list

    def parse_directory(self, log):
        mediainfo_list = []
        metadata_list = []
        metadata = {}

        for count, file_path in enumerate(self.file_paths):
            log.info("File {} out of {}: ".format(
                count + 1, len(self.file_paths)) + self.filenames[count])
            mediainfo_list.append(file_info(file_path))
            metadata = generate_hash(file_path)
            metadata['filename'] = self.filenames[count]
            metadata_list.append(metadata)
        return metadata_list, mediainfo_list, self.file_paths


def main(dir_path, log):
    try:
        parser = HashParser(dir_path)
        start_time = datetime.now()
        metadata_list, mediainfo_list, file_paths = parser.parse_directory(log)
        execution_time = (datetime.now() - start_time).total_seconds()
        for i in metadata_list:
            total_speed = (i['size'] / (1024 * 1014)) / execution_time
        log.info("Total hashing speed: {0:.2f} MB/sec".format(total_speed))
        filedata_list, animedata = fetch_anime_data(metadata_list, mediainfo_list,file_paths ,log)

        filedata = average_values(filedata_list, log)
        dump_to_file(filedata, animedata)

    except KeyboardInterrupt:
        log.error("Program Interrupted.")
