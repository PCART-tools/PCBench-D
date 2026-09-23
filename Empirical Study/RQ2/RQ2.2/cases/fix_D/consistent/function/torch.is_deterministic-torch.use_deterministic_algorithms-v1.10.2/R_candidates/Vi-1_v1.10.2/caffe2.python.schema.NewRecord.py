def NewRecord(net, schema):
    """
    Given a record of np.arrays, create a BlobReference for each one of them,
    returning a record containing BlobReferences. The name of each returned blob
    is NextScopedBlob(field_name), which guarantees unique name in the current
    net. Use NameScope explicitly to avoid name conflictions between different
    nets.
    """
    if isinstance(schema, Scalar):
        result = schema.clone()
        result.set_value(
            blob=net.NextScopedBlob('unnamed_scalar'),
            unsafe=True,
        )
        return result

    assert isinstance(schema, Field), 'Record must be a schema.Field instance.'
    blob_refs = [
        net.NextScopedBlob(prefix=name)
        for name in schema.field_names()
    ]
    return from_blob_list(schema, blob_refs)
