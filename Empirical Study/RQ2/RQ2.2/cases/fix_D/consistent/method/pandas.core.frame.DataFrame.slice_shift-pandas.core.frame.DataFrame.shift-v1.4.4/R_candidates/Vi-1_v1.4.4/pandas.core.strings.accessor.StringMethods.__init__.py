    def __init__(self, data):
        from pandas.core.arrays.string_ import StringDtype

        self._inferred_dtype = self._validate(data)
        self._is_categorical = is_categorical_dtype(data.dtype)
        self._is_string = isinstance(data.dtype, StringDtype)
        self._data = data

        self._index = self._name = None
        if isinstance(data, ABCSeries):
            self._index = data.index
            self._name = data.name

        # ._values.categories works for both Series/Index
        self._parent = data._values.categories if self._is_categorical else data
        # save orig to blow up categoricals to the right type
        self._orig = data
        self._freeze()
