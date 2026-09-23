def GetBlobs(meta_net_def, key):
    blobs = _ProtoMapGet(meta_net_def.blobs, key)
    if blobs is None:
        return []
    return blobs
