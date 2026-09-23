    def __init__(self, data, orig):
        if not isinstance(data, ABCSeries):
            raise TypeError("cannot convert an object of type {0} to a "
                            "datetimelike index".format(type(data)))

        self.values = data
        self.orig = orig
        self.name = getattr(data, 'name', None)
        self.index = getattr(data, 'index', None)
        self._freeze()
