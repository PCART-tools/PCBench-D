def SetRequestOnlyEmbeddings(meta_net_def, request_only_embeddings):
    for blob in request_only_embeddings:
        meta_net_def.requestOnlyEmbeddings.append(blob)
