from pymediainfo import MediaInfo

media_keys = [
    (1, 'frame_rate'),
    (1, 'other_display_aspect_ratio'),
    (2, 'other_sampling_rate'),
    (2, 'other_channel_s'),
    (3, 'format')]

def get_media_info(index, key, media_info):
    try:
        return media_info['tracks'][index][key]
    except IndexError:
        return "Not Found."

def file_info(file_path):
    media_info = MediaInfo.parse(file_path).to_data()

    local_file_info = [get_media_info(*keys, media_info) for keys in media_keys]

    return [i[0] if type(i) == list else i for i in local_file_info]

