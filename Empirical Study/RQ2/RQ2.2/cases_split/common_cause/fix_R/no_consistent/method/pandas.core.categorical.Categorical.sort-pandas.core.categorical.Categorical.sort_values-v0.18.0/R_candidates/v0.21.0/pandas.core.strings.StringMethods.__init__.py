    def __init__(self, data):
        self._is_categorical = is_categorical_dtype(data)
        self._data = data.cat.categories if self._is_categorical else data
        # save orig to blow up categoricals to the right type
        self._orig = data
        self._freeze()
