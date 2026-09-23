def FetchRecord(blob_record, ws=None, throw_on_type_mismatch=False):
    """
    Given a record containing BlobReferences, return a new record with same
    schema, containing numpy arrays, fetched from the current active workspace.
    """

    def fetch(v):
        if ws is None:
            return workspace.FetchBlob(str(v))
        else:
            return ws.blobs[str(v)].fetch()

    assert isinstance(blob_record, Field)
    field_blobs = blob_record.field_blobs()
    assert all(isinstance(v, BlobReference) for v in field_blobs)
    field_arrays = [fetch(value) for value in field_blobs]
    return from_blob_list(blob_record, field_arrays, throw_on_type_mismatch)
