    def __init__(self, values) -> None:
        super().__init__(values)
        self._dtype = StringDtype(storage=self._storage)

        if not pa.types.is_string(self._pa_array.type) and not (
            pa.types.is_dictionary(self._pa_array.type)
            and pa.types.is_string(self._pa_array.type.value_type)
        ):
            raise ValueError(
                "ArrowStringArray requires a PyArrow (chunked) array of string type"
            )
