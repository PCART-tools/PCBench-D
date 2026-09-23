def builtin_dict_keys(d):
    # Avoids overridden keys method of the dictionary
    assert isinstance(d, dict)
    return dict.keys(d)
