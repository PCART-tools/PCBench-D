def count_blobs(proto):
    blobs = set()
    for op in proto.op:
        blobs = blobs.union(set(op.input)).union(set(op.output))
    return len(blobs)
