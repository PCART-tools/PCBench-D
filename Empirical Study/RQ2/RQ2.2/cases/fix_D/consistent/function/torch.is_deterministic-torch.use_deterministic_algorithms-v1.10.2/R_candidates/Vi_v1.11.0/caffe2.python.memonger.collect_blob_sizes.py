def collect_blob_sizes(net):
    blobs = {}
    for op in net.op:
        for blob in op.input:
            blobs[blob] = blob_nbytes(blob)
        for blob in op.output:
            blobs[blob] = blob_nbytes(blob)

    return blobs
