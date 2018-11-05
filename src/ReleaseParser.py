def release_check(filedata_list, log):
        data = filedata_list

        animeid_list = []
        groupid_list = []
        resolution_list = []

        for filedata in data:
                animeid_list.append(filedata.anime_id)
                groupid_list.append(filedata.group_id)
                resolution_list.append(filedata.resolution)

        if  (all(x==animeid_list[0] for x in animeid_list) and
            all(x==groupid_list[0] for x in groupid_list) and
            all(x==resolution_list[0] for x in resolution_list)):
                return True
