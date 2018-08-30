def dump_to_file(filedata, animedata):
    with open("data.txt", 'w') as file:
            file.write("Show information\n\n")
            file.write("Year: " + animedata['year'] + '\n')
            file.write("Runtime: " + animedata['episode_count'] + " episodes.\n")
            file.write("Categories: " + animedata['categories'] + '\n')
            file.write("ANN Link: " + "https://www.animenewsnetwork.com/encyclopedia/anime.php?id={}".format(animedata['ANN_id']) + '\n')
            file.write("AniDB Link: " + "https://anidb.net/perl-bin/animedb.pl?show=anime&aid={}".format(animedata['anime_id']) + '\n')

            file.write("\nFile Information\n\n")
            file.write("Group link: http://anidb.net/perl-bin/animedb.pl?show=group&gid={}\n".format(filedata['group_id']))
            file.write("Source: " + filedata['source'] + '\n')
            file.write("Format: " + filedata['file_format'] + '\n')
            file.write("Release link: http://anidb.net/perl-bin/animedb.pl?show=group&gid={}&aid={}\n".format(filedata['group_id'], animedata['anime_id']))

            file.write("\nVideo\n\n")
            file.write("Resolution: " + filedata['resolution'] + '\n')
            file.write("Encoding: " + filedata['video_codec'] + '\n')
            file.write("Bitrate: " + filedata['video_bitrate'] + '\n')
            file.write("Color Depth: " + filedata['color_depth'] + '\n')

            file.write("\nAudio\n\n")
            file.write("Language: " + filedata['audio_language'] + '\n')
            file.write("Format: " + filedata['audio_codec'] + '\n')
            file.write("Bitrate: " + filedata['audio_bitrate'] + '\n')

            file.write("\nSubtitles\n\n")
            file.write("Language: " + filedata['sub_language'] + '\n')
