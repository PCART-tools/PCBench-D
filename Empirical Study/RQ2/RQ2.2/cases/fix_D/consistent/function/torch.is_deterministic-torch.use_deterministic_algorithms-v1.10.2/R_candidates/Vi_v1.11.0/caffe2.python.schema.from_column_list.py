def from_column_list(
    col_names, col_types=None,
    col_blobs=None, col_metadata=None
):
    """
    Given a list of names, types, and optionally values, construct a Schema.
    """
    if col_types is None:
        col_types = [None] * len(col_names)
    if col_metadata is None:
        col_metadata = [None] * len(col_names)
    if col_blobs is None:
        col_blobs = [None] * len(col_names)
    assert len(col_names) == len(col_types), (
        'col_names and col_types must have the same length.'
    )
    assert len(col_names) == len(col_metadata), (
        'col_names and col_metadata must have the same length.'
    )
    assert len(col_names) == len(col_blobs), (
        'col_names and col_blobs must have the same length.'
    )
    root = _SchemaNode('root', 'Struct')
    for col_name, col_type, col_blob, col_metadata in zip(
        col_names, col_types, col_blobs, col_metadata
    ):
        columns = col_name.split(FIELD_SEPARATOR)
        current = root
        for i in range(len(columns)):
            name = columns[i]
            type_str = ''
            field = None
            if i == len(columns) - 1:
                type_str = col_type
                field = Scalar(
                    dtype=col_type,
                    blob=col_blob,
                    metadata=col_metadata
                )
            next = current.add_child(name, type_str)
            if field is not None:
                next.field = field
            current = next

    return root.get_field()
