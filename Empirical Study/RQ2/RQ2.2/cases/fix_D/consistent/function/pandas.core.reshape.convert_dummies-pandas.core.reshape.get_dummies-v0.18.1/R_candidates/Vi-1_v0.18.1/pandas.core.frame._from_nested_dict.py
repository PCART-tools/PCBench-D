def _from_nested_dict(data):
    # TODO: this should be seriously cythonized
    new_data = OrderedDict()
    for index, s in compat.iteritems(data):
        for col, v in compat.iteritems(s):
            new_data[col] = new_data.get(col, OrderedDict())
            new_data[col][index] = v
    return new_data
