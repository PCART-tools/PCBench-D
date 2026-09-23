def urlencode(query, doseq=False):
    """
    A version of Python's urllib.parse.urlencode() function that can operate on
    MultiValueDict and non-string values.
    """
    if isinstance(query, MultiValueDict):
        query = query.lists()
    elif hasattr(query, 'items'):
        query = query.items()
    query_params = []
    for key, value in query:
        if isinstance(value, (str, bytes)):
            query_val = value
        else:
            try:
                iter(value)
            except TypeError:
                query_val = value
            else:
                # Consume generators and iterators, even when doseq=True, to
                # work around https://bugs.python.org/issue31706.
                query_val = [
                    item if isinstance(item, bytes) else str(item)
                    for item in value
                ]
        query_params.append((key, query_val))
    return original_urlencode(query_params, doseq)
