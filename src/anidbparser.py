import yumemi
import settings
import progressbar

from releaseparser import release_check

def fetch_anime_data(metadata_list):
    filedata_list = []
    animedata = {}
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
                                        'amask': 'A2000000',
                                        's': 'xxxxxx'})
        if response.code != 220:
            print(response.message)
            return 0,0

        file_data = {"file_id": response.data[0][0],
                    "anime_id": response.data[0][1],
                    "episode_id":response.data[0][2],
                    "group_id": response.data[0][3],
                    "is_deprecated": response.data[0][4],
                    "crc_hash": response.data[0][5],
                    "color_depth": response.data[0][6],
                    "source": response.data[0][7],
                    "audio_codec": response.data[0][8],
                    "audio_bitrate": response.data[0][9],
                    "video_codec": response.data[0][10],
                    "video_bitrate": response.data[0][11],
                    "resolution": response.data[0][12],
                    "file_format": response.data[0][13],
                    "audio_language": response.data[0][14],
                    "sub_language": response.data[0][15]}

        filedata_list.append(file_data)

    if not release_check(filedata_list):
        print("Release check failed! Either resolution, anime id or group id don't match for all files!")
        return 0,0

    anime_id = response.data[0][1]
    #animedata = {"episode_count": response.data[0][16],
    #            "year": response.data[0][17],
    #            "categories": response.data[0][18]}

    response = client.call("ANIME", {'aid': anime_id, 'amask': 'B2A08000400000', 's': 'xxxxx'})

    if response.code != 230:
        print(response.message)
        return 0,0
    animedata = {"anime_id": response.data[0][0],
                "year": response.data[0][1],
                "type": response.data[0][2],
                "categories": response.data[0][3],
                "romaji_name": response.data[0][4],
                "english_name": response.data[0][5],
                "episode_count": response.data[0][6],
                "ANN_id": response.data[0][7]}


    if len(metadata_list) < int(animedata['episode_count']):
        print("\nVerification failed!\nFile count in directory is lower than number of episodes on AniDB! Maybe your version is missing something?")
        return 0,0

    client.logout()
    if client.is_logged_in():
        print('Still logged in... Something went wrong!')
        return 0,0

    return filedata_list, animedata
