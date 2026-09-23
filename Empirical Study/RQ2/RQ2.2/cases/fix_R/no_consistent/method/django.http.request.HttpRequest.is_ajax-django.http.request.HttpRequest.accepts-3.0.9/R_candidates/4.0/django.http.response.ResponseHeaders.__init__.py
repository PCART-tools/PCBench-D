    def __init__(self, data):
        """
        Populate the initial data using __setitem__ to ensure values are
        correctly encoded.
        """
        if not isinstance(data, Mapping):
            data = {k: v for k, v in _destruct_iterable_mapping_values(data)}
        self._store = {}
        for header, value in data.items():
            self[header] = value
