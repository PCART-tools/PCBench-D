def count_shared_blobs(proto):
    blobs = set()
    for op in proto.op:
        blobs = blobs.union(set(op.input)).union(set(op.output))
    return len([b for b in blobs if "_shared" in b])
