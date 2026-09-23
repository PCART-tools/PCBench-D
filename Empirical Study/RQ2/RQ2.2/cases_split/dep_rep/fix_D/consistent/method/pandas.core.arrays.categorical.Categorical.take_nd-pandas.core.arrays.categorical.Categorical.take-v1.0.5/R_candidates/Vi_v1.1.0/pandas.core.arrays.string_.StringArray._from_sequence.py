    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        if dtype:
            assert dtype == "string"

        result = np.asarray(scalars, dtype="object")
        if copy and result is scalars:
            result = result.copy()

        # Standardize all missing-like values to NA
        # TODO: it would be nice to do this in _validate / lib.is_string_array
        # We are already doing a scan over the values there.
        na_values = isna(result)
        has_nans = na_values.any()
        if has_nans and result is scalars:
            # force a copy now, if we haven't already
            result = result.copy()

        # convert to str, then to object to avoid dtype like '<U3', then insert na_value
        result = np.asarray(result, dtype=str)
        result = np.asarray(result, dtype="object")
        if has_nans:
            result[na_values] = StringDtype.na_value

        return cls(result)
