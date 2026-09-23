def namedtupledict(typename, field_names, *args, **kwargs):
    field_names_map = {n: i for i, n in enumerate(field_names)}
    # Some output names are invalid python identifier, e.g. "0"
    kwargs.setdefault('rename', True)
    data = namedtuple(typename, field_names, *args, **kwargs)

    def getitem(self, key):
        if isinstance(key, string_types):
            key = field_names_map[key]
        return super(type(self), self).__getitem__(key)

    data.__getitem__ = getitem
    return data
