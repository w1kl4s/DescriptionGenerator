from src import ExceptionHandlers

def calculate_track(bitrate_list):
    if type(bitrate_list[0]) == str:
        bitrate_list = [int(x) for x in bitrate_list]
        return round(sum(bitrate_list)/len(bitrate_list))
    track_count = len(bitrate_list[0])
    #additional check performed here. All files should have same amount of audio and video tracks.
    for file_bitrates in bitrate_list:
        if len(file_bitrates) != track_count:
            raise ExceptionHandlers.ReleaseCheckException
    average_bitrates = [round(sum(map(int, i))/len(bitrate_list)) for i in zip(*bitrate_list)]
    return average_bitrates
def parse_tracks(filedata_list, log):
    video_bitrate_list = []
    audio_bitrate_list = []
    average_video_bitrate = []
    average_audio_bitrate = []
    for filedata in filedata_list:
        video_bitrate_list.append(filedata.video_bitrate)
        audio_bitrate_list.append(filedata.audio_bitrate)
    average_video_bitrate = calculate_track(video_bitrate_list)
    average_audio_bitrate = calculate_track(audio_bitrate_list)

    log.debug("averaged audio bitrates: {}".format(average_audio_bitrate))
    log.debug("averaged video bitrates: {}".format(average_video_bitrate))

    audio_languages = []
    audio_bitrate_string = ""
    video_bitrate_string = str(average_video_bitrate) + " kbps"
    if len(average_audio_bitrate) > 1:
        for filedata in filedata_list:
            for language in filedata.audio_language:
                if language not in audio_languages:
                    audio_languages.append(language)
        for track in range(0, len(average_audio_bitrate)):
            audio_bitrate_string += "{} : {} kbps, ".format(audio_languages[track], average_audio_bitrate[track]) 
        audio_bitrate_string = audio_bitrate_string[:-2]
    else:
        audio_bitrate_string = str(average_audio_bitrate[0]) + " kbps"

    languages = ', '.join(str(x) for x in audio_languages)

    return video_bitrate_string, audio_bitrate_string, languages, audio_languages

def average_values(filedata_list, log):
    video_string, audio_string, languages, languages_list = parse_tracks(filedata_list, log)
    filedata = filedata_list[0]
    filedata = filedata._replace(audio_bitrate = audio_string)
    filedata = filedata._replace(video_bitrate = video_string)
    filedata = filedata._replace(audio_language = languages)

    audio_codecs = filedata.audio_codec.split('\'')
    audio_codecs_string = ""
    for i in range(0,len(audio_codecs)):
        audio_codecs_string += "{}: {}, ".format(languages_list[i], audio_codecs[i])
    audio_codecs_string = audio_codecs_string[:-2]
    filedata = filedata._replace(audio_codec = audio_codecs_string)
    log.debug("{}".format(filedata))
    return filedata
