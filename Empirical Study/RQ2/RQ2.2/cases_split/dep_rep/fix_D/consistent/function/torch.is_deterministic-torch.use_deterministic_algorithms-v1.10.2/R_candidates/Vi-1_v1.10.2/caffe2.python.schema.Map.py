def Map(
    keys,
    values,
    keys_name='keys',
    values_name='values',
    lengths_blob=None
):
    """A map is a List of Struct containing keys and values fields.
    Optionally, you can provide custom name for the key and value fields.
    """
    return List(
        Struct((keys_name, keys), (values_name, values)),
        lengths_blob=lengths_blob
    )
