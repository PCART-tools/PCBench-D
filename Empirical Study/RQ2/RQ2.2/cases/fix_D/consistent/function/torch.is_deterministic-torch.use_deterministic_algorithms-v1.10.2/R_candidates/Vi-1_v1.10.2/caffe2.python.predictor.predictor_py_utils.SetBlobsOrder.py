def SetBlobsOrder(meta_net_def, blobs_order):
    for blob in blobs_order:
        meta_net_def.blobsOrder.append(blob)
