def from_blob_list(schema, values, throw_on_type_mismatch=False):
    """
    Create a schema that clones the given schema, but containing the given
    list of values.
    """
    assert isinstance(schema, Field), 'Argument `schema` must be a Field.'
    if isinstance(values, BlobReference):
        values = [values]
    record = schema.clone_schema()
    scalars = record.all_scalars()
    assert len(scalars) == len(values), (
        'Values must have %d elements, got %d.' % (len(scalars), len(values))
    )
    for scalar, value in zip(scalars, values):
        scalar.set_value(value, throw_on_type_mismatch, unsafe=True)
    return record
