    def _validate_listlike(self, value, allow_object: bool = False):
        if isinstance(value, type(self)):
            return value

        if isinstance(value, list) and len(value) == 0:
            # We treat empty list as our own dtype.
            return type(self)._from_sequence([], dtype=self.dtype)

        if hasattr(value, "dtype") and value.dtype == object:
            # `array` below won't do inference if value is an Index or Series.
            #  so do so here.  in the Index case, inferred_type may be cached.
            if lib.infer_dtype(value) in self._infer_matches:
                try:
                    value = type(self)._from_sequence(value)
                except (ValueError, TypeError):
                    if allow_object:
                        return value
                    msg = self._validation_error_message(value, True)
                    raise TypeError(msg)

        # Do type inference if necessary up front (after unpacking
        # NumpyExtensionArray)
        # e.g. we passed PeriodIndex.values and got an ndarray of Periods
        value = extract_array(value, extract_numpy=True)
        value = pd_array(value)
        value = extract_array(value, extract_numpy=True)

        if is_all_strings(value):
            # We got a StringArray
            try:
                # TODO: Could use from_sequence_of_strings if implemented
                # Note: passing dtype is necessary for PeriodArray tests
                value = type(self)._from_sequence(value, dtype=self.dtype)
            except ValueError:
                pass

        if isinstance(value.dtype, CategoricalDtype):
            # e.g. we have a Categorical holding self.dtype
            if value.categories.dtype == self.dtype:
                # TODO: do we need equal dtype or just comparable?
                value = value._internal_get_values()
                value = extract_array(value, extract_numpy=True)

        if allow_object and is_object_dtype(value.dtype):
            pass

        elif not type(self)._is_recognized_dtype(value.dtype):
            msg = self._validation_error_message(value, True)
            raise TypeError(msg)

        return value
