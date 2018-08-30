import yumemi
import settings
import progressbar
import collections

from releaseparser import release_check

def fetch_anime_data(metadata_list):
    filedata_list = []
    anime_data = {}
    file_response_data = collections.namedtuple('file_data', ["file_id",
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
                                                     "sub_language"])
    anime_response_data = collections.namedtuple('anime_data', ["anime_id",
                                                                                                                "year",
                                                                                                                "type",
                                                                                                                "categories",
                                                                                                                "romaji_name",
                                                                                                                "english_name",
                                                                                                                "episode_count",
                                                                                                                "ANN_id"])


    client = yumemi.Client()
    client.auth(settings.login, settings.password)
    if settings.key:
        client.encrypt(settings.key, settings.login)

    print("\nQuerying hashes to AniDB...")

    for counter, metadata in enumerate(metadata_list):
        print(metadata['filename'] +  " is being processed..." + " (File {} out of {})".format(counter+1, len(metadata_list)))


        file_size = metadata['size']
        file_hash = metadata['hash']


        if not client.ping():
            print('AniDB is DOWN')
            return 0,0

        response = client.call('FILE', {'size': file_size,
                                        'ed2k': file_hash,
                                        'fmask': '720A7FC000',
                                        'amask': '00000000',
                                        's': 'xxxxxx'})
        if response.code != 220:
            print(response.message)
            return 0,0

        file_data = file_response_data(*response.data[0])

        filedata_list.append(file_data)

    if not release_check(filedata_list):
        print("Release check failed! Either resolution, anime id or group id don't match for all files!")
        return 0,0

    anime_id = file_data.anime_id

    response = client.call("ANIME", {'aid': anime_id, 'amask': 'B2A08000400000', 's': 'xxxxx'})

    if response.code != 230:
        print(response.message)
        return 0,0

    anime_data = anime_response_data(*response.data[0])

    if len(metadata_list) < int(anime_data.episode_count):
        print("\nVerification failed!\nFile count in directory is lower than number of episodes on AniDB! Maybe your version is missing something?")
        return 0,0

    client.logout()
    if client.is_logged_in():
        print('Still logged in... Something went wrong!')
        return 0,0

    return filedata_list, anime_data
