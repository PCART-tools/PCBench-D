    def __init__(self, values, copy=False):
        values = extract_array(values)

        super().__init__(values, copy=copy)
        # error: Incompatible types in assignment (expression has type "StringDtype",
        # variable has type "PandasDtype")
        NDArrayBacked.__init__(self, self._ndarray, StringDtype(storage="python"))
        if not isinstance(values, type(self)):
            self._validate()
