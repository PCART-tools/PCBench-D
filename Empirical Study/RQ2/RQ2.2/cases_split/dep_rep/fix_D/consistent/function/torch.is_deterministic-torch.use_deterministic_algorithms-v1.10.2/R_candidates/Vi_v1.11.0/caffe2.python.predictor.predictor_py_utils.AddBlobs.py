def AddBlobs(meta_net_def, blob_name, blob_def):
    blobs = _ProtoMapGet(meta_net_def.blobs, blob_name)
    if blobs is None:
        blobs = meta_net_def.blobs.add()
        blobs.key = blob_name
        blobs = blobs.value
    for blob in blob_def:
        blobs.append(blob)
