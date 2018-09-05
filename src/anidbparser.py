import yumemi
import settings
import progressbar
import collections

from releaseparser import release_check
from exceptionhandlers import AniDBDown, AniDBResponseException, ReleaseCheckException, FileCountError, LogoutError
from localmediainfo import file_info

FileResponseData = collections.namedtuple('file_data', [  "file_id",
                                                            "anime_id",
                                                            "episode_id",
                                                            "group_id",
                                                            "is_deprecated",
                                                            "crc_hash",
                                                            "color_depth",
                                                            "source",
                                                            "audio_codec",
                                                            "audio_bitrate",
                                                            "video_codec",
                                                            "video_bitrate",
                                                            "resolution",
                                                            "file_format",
                                                            "audio_language",
                                                            "sub_language",
                                                            "frame_rate",
                                                            "aspect_ratio",
                                                            "audio_sample_rate",
                                                            "audio_channels",
                                                            "sub_format"])
AnimeResponseData = collections.namedtuple('anime_data', ["anime_id",
                                                            "year",
                                                            "type",
                                                            "categories",
                                                            "romaji_name",
                                                            "english_name",
                                                            "episode_count",
                                                            "ANN_id"])

def fetch_anime_data(metadata_list, mediainfo_list, file_paths,log):
    filedata_list = []
    anime_data = {}

    client = yumemi.Client()
    client.auth(settings.login, settings.password)
    if settings.key:
        client.encrypt(settings.key, settings.login)

    log.info("Querying hashes to AniDB...")

    for counter, metadata in enumerate(metadata_list):
        log.info(metadata['filename'] +    " is being processed..." + " (File {} out of {})".format(counter+1, len(metadata_list)))


        file_size = metadata['size']
        file_hash = metadata['hash']


        if not client.ping():
            log.error("Client ping failed.")
            raise AniDBDown

        response = client.call('FILE', {'size': file_size,
                                        'ed2k': file_hash,
                                        'fmask': '720A7FC000',
                                        'amask': '00000000',
                                        's': 'xxxxxx'})
        if response.code != 220:
            log.error("Wrong response! File was not found.")
            raise AniDBResponseException(response.code)

        local_file_data = file_info(file_paths[counter])
        response.data[0].extend(local_file_data)

        file_data = FileResponseData(*response.data[0])

        filedata_list.append(file_data)

    if not release_check(filedata_list):
        log.error("Release check failed.")
        raise ReleaseCheckException

    anime_id = file_data.anime_id

    response = client.call("ANIME", {'aid': anime_id, 'amask': 'B2A08000400000', 's': 'xxxxx'})

    if response.code != 230:
        log.error("Wrong response! Anime was not found")
        raise AniDBResponseException(response.code)

    anime_data = AnimeResponseData(*response.data[0])

    if len(metadata_list) < int(anime_data.episode_count):
        log.error("File count is lower than expected.")
        raise FileCountError

    client.logout()
    if client.is_logged_in():
        log.error("Logout failed")
        raise LogoutError

    return filedata_list, anime_data
