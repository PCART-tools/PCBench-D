    def _get_common_dtype(self, dtypes: list[DtypeObj]) -> DtypeObj | None:
        # Handle only boolean + np.bool_ -> boolean, since other cases like
        # Int64 + boolean -> Int64 will be handled by the other type
        if all(
            isinstance(t, BooleanDtype)
            or (isinstance(t, np.dtype) and (np.issubdtype(t, np.bool_)))
            for t in dtypes
        ):
            return BooleanDtype()
        else:
            return None
