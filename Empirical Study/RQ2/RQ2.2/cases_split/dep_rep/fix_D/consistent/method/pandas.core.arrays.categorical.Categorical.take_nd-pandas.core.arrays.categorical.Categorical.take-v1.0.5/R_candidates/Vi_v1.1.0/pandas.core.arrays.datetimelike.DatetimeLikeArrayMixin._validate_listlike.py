    def _validate_listlike(
        self, value, opname: str, cast_str: bool = False, allow_object: bool = False
    ):
        if isinstance(value, type(self)):
            return value

        # Do type inference if necessary up front
        # e.g. we passed PeriodIndex.values and got an ndarray of Periods
        value = array(value)
        value = extract_array(value, extract_numpy=True)

        if cast_str and is_dtype_equal(value.dtype, "string"):
            # We got a StringArray
            try:
                # TODO: Could use from_sequence_of_strings if implemented
                # Note: passing dtype is necessary for PeriodArray tests
                value = type(self)._from_sequence(value, dtype=self.dtype)
            except ValueError:
                pass

        if is_categorical_dtype(value.dtype):
            # e.g. we have a Categorical holding self.dtype
            if is_dtype_equal(value.categories.dtype, self.dtype):
                # TODO: do we need equal dtype or just comparable?
                value = value._internal_get_values()

        if allow_object and is_object_dtype(value.dtype):
            pass

        elif not type(self)._is_recognized_dtype(value.dtype):
            raise TypeError(
                f"{opname} requires compatible dtype or scalar, "
                f"not {type(value).__name__}"
            )

        return value
