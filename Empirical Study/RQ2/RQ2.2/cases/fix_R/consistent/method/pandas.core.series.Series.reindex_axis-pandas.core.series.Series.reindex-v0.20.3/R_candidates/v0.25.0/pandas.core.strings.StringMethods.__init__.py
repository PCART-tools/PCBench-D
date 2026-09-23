    def __init__(self, data):
        self._inferred_dtype = self._validate(data)
        self._is_categorical = is_categorical_dtype(data)

        # .values.categories works for both Series/Index
        self._parent = data.values.categories if self._is_categorical else data
        # save orig to blow up categoricals to the right type
        self._orig = data
        self._freeze()
