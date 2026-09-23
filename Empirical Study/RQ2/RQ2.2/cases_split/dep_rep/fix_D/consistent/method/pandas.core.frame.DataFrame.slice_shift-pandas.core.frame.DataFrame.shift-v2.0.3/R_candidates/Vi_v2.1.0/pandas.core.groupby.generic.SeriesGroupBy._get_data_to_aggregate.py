    def _get_data_to_aggregate(
        self, *, numeric_only: bool = False, name: str | None = None
    ) -> SingleManager:
        ser = self._selected_obj
        single = ser._mgr
        if numeric_only and not is_numeric_dtype(ser.dtype):
            # GH#41291 match Series behavior
            kwd_name = "numeric_only"
            raise TypeError(
                f"Cannot use {kwd_name}=True with "
                f"{type(self).__name__}.{name} and non-numeric dtypes."
            )
        return single
