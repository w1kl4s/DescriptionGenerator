def plus_variation(average, total_list):
    return (max(total_list) / average - 1) * 100

def minus_variation(average, total_list):
    return (min(total_list) / average - 1) * 100

def average_values(filedata_list, log):
    video_bitrate_list = []
    audio_bitrate_list = []
    for file_data in filedata_list:
        video_bitrate_list.append(int(file_data.video_bitrate))
        audio_bitrate_list.append(int(file_data.audio_bitrate))

    average_video_bitrate = sum(video_bitrate_list) / len(video_bitrate_list)
    average_audio_bitrate = sum(audio_bitrate_list) / len(audio_bitrate_list)

    log.info("Average Video bitrate calculated. Video bitrate variation: +{:0.2f}% and {:1.2f}%".format(
                                                                                                        plus_variation(average_video_bitrate, video_bitrate_list),
                                                                                                        minus_variation(average_video_bitrate, video_bitrate_list)))
    log.info("Average Audio bitrate calculated. Audio bitrate variation: +{:0.2f}% and {:1.2f}%".format(
                                                                                                        plus_variation(average_audio_bitrate, audio_bitrate_list),
                                                                                                        minus_variation(average_audio_bitrate, audio_bitrate_list)))

    filedata = filedata_list[0]
    filedata._replace(video_bitrate = average_video_bitrate)
    filedata._replace(video_bitrate = average_video_bitrate)

    return filedata
