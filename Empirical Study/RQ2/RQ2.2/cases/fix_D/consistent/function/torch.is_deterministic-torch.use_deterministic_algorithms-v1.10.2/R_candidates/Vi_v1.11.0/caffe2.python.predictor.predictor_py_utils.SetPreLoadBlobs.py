def SetPreLoadBlobs(meta_net_def, pre_load_blobs):
    for blob in pre_load_blobs:
        meta_net_def.preLoadBlobs.append(blob)
