    def __init__(self, values):
        self._dtype = StringDtype(storage="pyarrow")
        if isinstance(values, pa.Array):
            self._data = pa.chunked_array([values])
        elif isinstance(values, pa.ChunkedArray):
            self._data = values
        else:
            raise ValueError(f"Unsupported type '{type(values)}' for ArrowStringArray")

        if not pa.types.is_string(self._data.type):
            raise ValueError(
                "ArrowStringArray requires a PyArrow (chunked) array of string type"
            )
