import yumemi
import settings
import progressbar
import collections
import requests
import xmltodict
from jikanpy import Jikan


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
                                                            "ANN_id",
                                                            "MAL_id",
                                                            "director_id",
                                                            "studio_id_list"])
def get_creator_info(anime_id):
    r = requests.get("http://api.anidb.net:9001/httpapi?request=anime&client=descgen&clientver=1&protover=1&aid={}".format(anime_id))

    anime_data = xmltodict.parse(r.content)

    studio_id_list = []
    for creator in anime_data['anime']['creators']['name']:
        if "direction" in creator['@type'].lower():
            director_id = creator['@id']
        if creator['@type'].lower() == "work" or creator['@type'].lower() == "animation work":
            studio_id_list.append(creator['@id'])
    return director_id, studio_id_list

def fetch_anime_data(metadata_list, mediainfo_list, file_paths,log):
    filedata_list = []
    anime_data = {}
    jikan = Jikan()

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

        response.data[0].extend(mediainfo_list[counter])

        file_data = FileResponseData(*response.data[0])

        if file_data.is_deprecated != "0":
            log.warning("File seems to be deprecated! is_depracated field from AniDB is {}!".format(file_data.is_deprecated))

        log.debug("file id: {}, video bitrate: {}, audio bitrate: {}, is deprecated: {}".format(file_data.file_id,
                                                                                                file_data.video_bitrate,
                                                                                                file_data.audio_bitrate,
                                                                                                file_data.is_deprecated))
        filedata_list.append(file_data)

    if not release_check(filedata_list, log):
        log.error("Release check failed.")
        raise ReleaseCheckException

    anime_id = file_data.anime_id



    response = client.call("ANIME", {'aid': anime_id, 'amask': 'B2A08000400000', 's': 'xxxxx'})

    if response.code != 230:
        log.error("Wrong response! Anime was not found")
        raise AniDBResponseException(response.code)

    mal_search_result = jikan.search('anime', response.data[0][5])['results'][0]['mal_id']

    director_id, studio_id_list = get_creator_info(response.data[0][0])

    response.data[0].append(mal_search_result)
    response.data[0].append(director_id)
    response.data[0].append(studio_id_list)

    anime_data = AnimeResponseData(*response.data[0])

    if len(metadata_list) < int(anime_data.episode_count):
        log.error("File count is lower than expected.")
        raise FileCountError

    client.logout()
    if client.is_logged_in():
        log.error("Logout failed")
        raise LogoutError

    for filedata in filedata_list:
        if filedata.sub_format == "Not Found.":
            log.warning("One or more files has missing subtitle format information! Check log for detailed information.")
            break
    return filedata_list, anime_data
