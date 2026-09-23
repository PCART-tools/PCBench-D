def ReplaceBlobs(meta_net_def, blob_name, blob_def):
    blobs = _ProtoMapGet(meta_net_def.blobs, blob_name)
    assert blobs is not None, "The blob_name:{} does not exist".format(blob_name)
    del blobs[:]
    for blob in blob_def:
        blobs.append(blob)
