def dict_keys_getitem(d, n):
    # Call dict(d) to prevent calling overridden __iter__/keys
    dict_class = dict
    if isinstance(d, OrderedDict):
        dict_class = OrderedDict
    return next(itertools.islice(dict_class.keys(d), n, n + 1))
