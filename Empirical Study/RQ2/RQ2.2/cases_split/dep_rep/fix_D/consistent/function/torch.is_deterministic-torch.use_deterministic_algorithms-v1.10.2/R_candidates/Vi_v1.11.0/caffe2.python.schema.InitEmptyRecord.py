def InitEmptyRecord(net, schema_or_record, enforce_types=False):
    if not schema_or_record.has_blobs():
        record = NewRecord(net, schema_or_record)
    else:
        record = schema_or_record

    for blob_type, blob in zip(record.field_types(), record.field_blobs()):
        try:
            data_type = data_type_for_dtype(blob_type)
            shape = [0] + list(blob_type.shape)
            net.ConstantFill([], blob, shape=shape, dtype=data_type)
        except TypeError:
            logger.warning("Blob {} has type error".format(blob))
            # If data_type_for_dtype doesn't know how to resolve given numpy
            # type to core.DataType, that function can throw type error (for
            # example that would happen for cases of unknown types such as
            # np.void). This is not a problem for cases when the record if going
            # to be overwritten by some operator later, though it might be an
            # issue for type/shape inference.
            if enforce_types:
                raise
            # If we don't enforce types for all items we'll create a blob with
            # the default ConstantFill (FLOAT, no shape)
            net.ConstantFill([], blob, shape=[0])

    return record
