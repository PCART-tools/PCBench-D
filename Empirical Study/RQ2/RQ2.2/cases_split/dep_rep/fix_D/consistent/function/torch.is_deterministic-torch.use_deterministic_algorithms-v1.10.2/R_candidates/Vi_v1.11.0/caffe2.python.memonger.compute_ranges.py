def compute_ranges(linearized_ops, blob_sizes=None):
    if not blob_sizes:
        log.warning('Provide blob sizes to get more accurate assignments.')

    blobs = collections.defaultdict(
        lambda: LiveRange(defined=None, used=None, size=None))
    for i, op in enumerate(linearized_ops):
        for blob in op.input:
            used = blobs[blob].used
            if used is None:
                used = i
            else:
                used = max(used, i)
            blobs[blob] = blobs[blob]._replace(used=used)
            blob_size = blob_sizes[blob] if blob_sizes else None
            assert not blob_sizes or blob_size is not None
            blobs[blob] = blobs[blob]._replace(size=blob_size)
        for blob in op.output:
            defined = blobs[blob].defined
            if defined is None:
                defined = i
            else:
                defined = min(defined, i)
            blobs[blob] = blobs[blob]._replace(defined=defined)
            blob_size = blob_sizes[blob] if blob_sizes else None
            assert not blob_sizes or blob_size is not None
            blobs[blob] = blobs[blob]._replace(size=blob_size)

    return blobs
