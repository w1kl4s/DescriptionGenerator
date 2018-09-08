import sys
import os
import datetime
import json

from src import Ed2k
from src import AnidbParser
from src import FileWrite
from src import LocalMediaInfo
from src import Averages

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
    def sum_time(self, execution_time_list):
        time_sum = datetime.timedelta()
        for i in execution_time_list:
            i = str(i)
            (h, m, s) = i.split(':')
            d = datetime.timedelta(hours=float(h), minutes=float(m), seconds=float(s))
            time_sum += d
        return time_sum.total_seconds()

    def parse_directory(self, log):
        mediainfo_list = []
        metadata_list = []
        metadata = {}
        execution_time_list = []

        for count, file_path in enumerate(self.file_paths):
            log.info("File {} out of {}: ".format(
                                                count + 1,
                                                len(self.file_paths)) + self.filenames[count])
            mediainfo_list.append(LocalMediaInfo.file_info(file_path, log))

            start_time = datetime.datetime.now()
            metadata = Ed2k.generate_hash(file_path, log)
            execution_time_list.append(datetime.datetime.now() - start_time)
            log.debug("Hashing time: {0:.2f} seconds.".format((datetime.datetime.now() - start_time).total_seconds()))

            metadata['filename'] = self.filenames[count]
            metadata_list.append(metadata)

        execution_time = self.sum_time(execution_time_list)
        log.debug("Total hashing time: {0:.2f} seconds.".format(execution_time))

        return metadata_list, mediainfo_list, self.file_paths, execution_time

def main(dir_path, log):
    try:
        parser = HashParser(dir_path)
        metadata_list, mediainfo_list, file_paths, execution_time = parser.parse_directory(log)
        for i in metadata_list:
            total_speed = (i['size'] / (1024 * 1014)) / execution_time
        log.info("Total hashing speed: {0:.2f} MB/sec".format(total_speed))
        filedata_list, animedata = AnidbParser.fetch_anime_data(metadata_list, mediainfo_list,file_paths ,log)

        filedata = Averages.average_values(filedata_list, log)
        FileWrite.dump_to_file(filedata, animedata, log)

    except KeyboardInterrupt:
        log.error("Program Interrupted.")
