def reverse_dict(dict):
    newdict = {}
    sorted_keys = list(dict.keys())
    sorted_keys.sort()
    for key in sorted_keys[::-1]:
        newdict[dict[key]] = key
    return newdict
