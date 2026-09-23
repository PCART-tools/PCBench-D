    def _check_fill_value(self):
        if not lib.is_scalar(self._fill_value):
            raise ValueError(
                f"fill_value must be a scalar. Got {self._fill_value} instead"
            )

        from pandas.core.dtypes.cast import can_hold_element
        from pandas.core.dtypes.missing import (
            is_valid_na_for_dtype,
            isna,
        )

        from pandas.core.construction import ensure_wrapped_if_datetimelike

        # GH#23124 require fill_value and subtype to match
        val = self._fill_value
        if isna(val):
            if not is_valid_na_for_dtype(val, self.subtype):
                warnings.warn(
                    "Allowing arbitrary scalar fill_value in SparseDtype is "
                    "deprecated. In a future version, the fill_value must be "
                    "a valid value for the SparseDtype.subtype.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
        else:
            dummy = np.empty(0, dtype=self.subtype)
            dummy = ensure_wrapped_if_datetimelike(dummy)

            if not can_hold_element(dummy, val):
                warnings.warn(
                    "Allowing arbitrary scalar fill_value in SparseDtype is "
                    "deprecated. In a future version, the fill_value must be "
                    "a valid value for the SparseDtype.subtype.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
