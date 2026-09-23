    def __init__(self, values, copy=False):
        values = extract_array(values)
        skip_validation = isinstance(values, type(self))

        super().__init__(values, copy=copy)
        self._dtype = StringDtype()
        if not skip_validation:
            self._validate()
