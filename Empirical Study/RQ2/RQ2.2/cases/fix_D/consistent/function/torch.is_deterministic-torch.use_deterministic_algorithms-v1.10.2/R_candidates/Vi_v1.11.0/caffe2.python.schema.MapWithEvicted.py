def MapWithEvicted(
    keys,
    values,
    keys_name='keys',
    values_name='values',
    lengths_blob=None,
    evicted_values=None
):
    """A map with extra field evicted_values
    """
    return ListWithEvicted(
        Struct((keys_name, keys), (values_name, values)),
        lengths_blob=lengths_blob,
        evicted_values=evicted_values
    )
