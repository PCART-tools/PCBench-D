def FeedRecord(blob_record, arrays, ws=None):
    """
    Given a Record containing blob_references and arrays, which is either
    a list of numpy arrays or a Record containing numpy arrays, feeds the
    record to the current workspace.
    """

    def feed(b, v):
        if ws is None:
            workspace.FeedBlob(str(b), v)
        else:
            ws.create_blob(str(b))
            ws.blobs[str(b)].feed(v)
    assert isinstance(blob_record, Field)
    field_blobs = blob_record.field_blobs()
    assert all(isinstance(v, BlobReference) for v in field_blobs)
    if isinstance(arrays, Field):
        # TODO: check schema
        arrays = arrays.field_blobs()
    assert len(arrays) == len(field_blobs), (
        'Values must contain exactly %d ndarrays.' % len(field_blobs)
    )
    for blob, array in zip(field_blobs, arrays):
        feed(blob, array)
