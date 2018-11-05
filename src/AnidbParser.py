import yumemi
import progressbar
import collections
import requests
import xmltodict
from jikanpy import Jikan

from src import ReleaseParser
from src import ExceptionHandlers

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
                                                            "group_name",
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
                                                            "director_link",
                                                            "studio_links"])
def get_creator_links(anime_id, log):

    director_data, studio_data_list = get_creator_info(anime_id, log)

    director_link = ('</b> <a href="https://anidb.net/perl-bin/animedb.pl?'
                    'show=creator&creatorid={}">{}</a>').format(director_data[0], director_data[1])

    studio_link_list = []
    for studio_data in studio_data_list:
        studio_link_list.append(('</b> <a href="https://anidb.net/perl-bin/animedb.pl?'
                                'show=creator&creatorid={}">{}</a>').format(studio_data[0], studio_data[1]))

    studio_links = ""
    if len(studio_link_list) == 1:
        studio_links = studio_link_list[0]
    else:
        for studio_link in studio_link_list:
            studio_links += studio_links + ', '

    return director_link, studio_links
def get_creator_info(anime_id, log):
    r = requests.get("http://api.anidb.net:9001/httpapi?request=anime&client=descgen&clientver=1&protover=1&aid={}".format(anime_id))

    anime_data = xmltodict.parse(r.content)

    studio_data_list = []
    director_data = 0
    try:
        for creator in anime_data['anime']['creators']['name']:
            if creator['@type'].lower() == "direction":
                director_data = [creator['@id'], creator['#text']]
            if creator['@type'].lower() == "work" or creator['@type'].lower() == "animation work":
                studio_data_list.append([creator['@id'], creator['#text']])
    except KeyError:
        raise ExceptionHandlers.HTTPApiError
    if studio_data_list == []:
        log.error("Studio was not found! Fill it out manually!")
        studio_data_list == ["Not Found.", "Not Found."]
    if director_data == 0:
        log.error("Director was not found! Fill it out manually!")
        director_data = ["Not Found.", "Not Found."]
    return director_data, studio_data_list

def fetch_anime_data(metadata_list, mediainfo_list, file_paths,log):
    try:
        import settings
    except ModuleNotFoundError:
        log.error("Settings file not found! Something has gone terribly wrong!")
        raise SettingsVanishedError

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
            raise ExceptionHandlers.AniDBDown

        response = client.call('FILE', {'size': file_size,
                                        'ed2k': file_hash,
                                        'fmask': '720A7FC000',
                                        'amask': '00000080',
                                        's': 'xxxxxx'})
        if response.code != 220:
            log.error("Wrong response! File was not found.")
            raise ExceptionHandlers.AniDBResponseException(response.code)

        response.data[0].extend(mediainfo_list[counter])

        file_data = FileResponseData(*response.data[0])

        if file_data.is_deprecated != "0":
            log.warning("File seems to be deprecated! is_depracated field from AniDB is {}!".format(file_data.is_deprecated))

        # Small workaround for files with multiple audio tracks. Makes it easier to parse those later.

        file_data = file_data._replace(audio_language = file_data.audio_language.split('\''))
        file_data = file_data._replace(audio_bitrate = file_data.audio_bitrate.split('\''))

        log.debug("file id: {}, video bitrate: {}"
                     ", audio bitrate: {}, audio language: {}"
                     ",is deprecated: {}".format(file_data.file_id,
                                                    file_data.video_bitrate,
                                                    file_data.audio_bitrate,
                                                    file_data.audio_language,
                                                    file_data.is_deprecated))
        filedata_list.append(file_data)
    if not ReleaseParser.release_check(filedata_list, log):
        log.error("Release check failed.")
        raise ExceptionHandlers.ReleaseCheckException
    else:
        log.info("Release check successful.")

    anime_id = file_data.anime_id

    response = client.call("ANIME", {'aid': anime_id, 'amask': 'B2A08000400000', 's': 'xxxxx'})    

    if response.code != 230:
        log.error("Wrong response! Anime was not found")
        raise AniDBResponseException(response.code)

    mal_search_result = jikan.search('anime', response.data[0][5])['results'][0]['mal_id']

    director_link, studio_links = get_creator_links(response.data[0][0], log)

    response.data[0].append(mal_search_result)
    response.data[0].append(director_link)
    response.data[0].append(studio_links)

    anime_data = AnimeResponseData(*response.data[0])

    log.debug(studio_links)

    if len(metadata_list) < int(anime_data.episode_count):
        log.error("File count is lower than expected.")
        raise ExceptionHandlers.FileCountError

    client.logout()
    if client.is_logged_in():
        log.error("Logout failed")
        raise ExceptionHandlers.LogoutError

    for filedata in filedata_list:
        if filedata.sub_format == "Not Found.":
            log.warning("One or more files has missing subtitle format information! Check log for detailed information.")
            break
    return filedata_list, anime_data
