def ConstRecord(net, array_record):
    """
    Given a record of arrays, returns a record of blobs,
    initialized with net.Const.
    """
    blob_record = NewRecord(net, array_record)
    for blob, array in zip(
        blob_record.field_blobs(), array_record.field_blobs()
    ):
        net.Const(array, blob)
    return blob_record
