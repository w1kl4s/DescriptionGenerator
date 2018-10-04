import os

def dump_to_file(filedata, animedata, log):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../templates/basictemplate.html", 'r') as file:
        template = file.read()
    with open(dir_path + "/../Generated Descriptions/" + animedata.english_name + ".html", 'w') as file:
        log.debug("{}".format(animedata))
        file.write(template.format( year = animedata.year,
                                    episode_count = animedata.episode_count,
                                    categories = animedata.categories,
                                    director_link = animedata.director_link,
                                    studio_links = animedata.studio_links,
                                    ANN_id = animedata.ANN_id,
                                    anime_id = animedata.anime_id,
                                    MAL_id = animedata.MAL_id,
                                    group_id = filedata.group_id,
                                    group_name = filedata.group_name,
                                    source = filedata.source,
                                    file_format = filedata.file_format,
                                    resolution = filedata.resolution,
                                    video_codec = filedata.video_codec,
                                    frame_rate = filedata.frame_rate,
                                    video_bitrate = filedata.video_bitrate,
                                    color_depth = filedata.color_depth,
                                    aspect_ratio = filedata.aspect_ratio,
                                    audio_language = filedata.audio_language,
                                    audio_channels = filedata.audio_channels,
                                    audio_codec = filedata.audio_codec,
                                    audio_sample_rate = filedata.audio_sample_rate,
                                    audio_bitrate = filedata.audio_bitrate,
                                    sub_language = filedata.sub_language,
                                    sub_format = filedata.sub_format,
                                    english_name = animedata.english_name))
    log.debug("File written.")
