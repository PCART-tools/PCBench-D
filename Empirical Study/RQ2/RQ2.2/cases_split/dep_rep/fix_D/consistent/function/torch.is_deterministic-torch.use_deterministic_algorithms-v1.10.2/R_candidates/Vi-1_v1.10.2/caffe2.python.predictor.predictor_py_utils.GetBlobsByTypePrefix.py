def GetBlobsByTypePrefix(meta_net_def, blob_type_prefix):
    blob_map = {}
    for b in meta_net_def.blobs:
        if b.key.startswith(blob_type_prefix):
            for blob in b.value:
                if blob not in blob_map:
                    blob_map[blob] = len(blob_map)
    return sorted(blob_map, key=lambda blob: blob_map[blob])
