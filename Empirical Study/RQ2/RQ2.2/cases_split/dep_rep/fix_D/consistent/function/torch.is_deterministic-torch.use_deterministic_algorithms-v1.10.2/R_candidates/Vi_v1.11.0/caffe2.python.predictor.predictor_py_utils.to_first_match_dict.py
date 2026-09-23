def to_first_match_dict(kv_list):
    """
    Construct dict from kv_list
    """
    d = {}
    for item in kv_list:
        if item.key not in d:
            d[item.key] = item.value
    return d
