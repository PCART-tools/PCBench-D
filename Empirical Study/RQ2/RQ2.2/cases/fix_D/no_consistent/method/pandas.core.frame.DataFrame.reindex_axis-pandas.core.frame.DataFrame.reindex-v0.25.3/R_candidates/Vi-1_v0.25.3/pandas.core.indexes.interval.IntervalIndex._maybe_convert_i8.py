    def _maybe_convert_i8(self, key):
        """
        Maybe convert a given key to it's equivalent i8 value(s). Used as a
        preprocessing step prior to IntervalTree queries (self._engine), which
        expects numeric data.

        Parameters
        ----------
        key : scalar or list-like
            The key that should maybe be converted to i8.

        Returns
        -------
        key: scalar or list-like
            The original key if no conversion occured, int if converted scalar,
            Int64Index if converted list-like.
        """
        original = key
        if is_list_like(key):
            key = ensure_index(key)

        if not self._needs_i8_conversion(key):
            return original

        scalar = is_scalar(key)
        if is_interval_dtype(key) or isinstance(key, Interval):
            # convert left/right and reconstruct
            left = self._maybe_convert_i8(key.left)
            right = self._maybe_convert_i8(key.right)
            constructor = Interval if scalar else IntervalIndex.from_arrays
            return constructor(left, right, closed=self.closed)

        if scalar:
            # Timestamp/Timedelta
            key_dtype, key_i8 = infer_dtype_from_scalar(key, pandas_dtype=True)
        else:
            # DatetimeIndex/TimedeltaIndex
            key_dtype, key_i8 = key.dtype, Index(key.asi8)
            if key.hasnans:
                # convert NaT from it's i8 value to np.nan so it's not viewed
                # as a valid value, maybe causing errors (e.g. is_overlapping)
                key_i8 = key_i8.where(~key._isnan)

        # ensure consistency with IntervalIndex subtype
        subtype = self.dtype.subtype
        msg = (
            "Cannot index an IntervalIndex of subtype {subtype} with "
            "values of dtype {other}"
        )
        if not is_dtype_equal(subtype, key_dtype):
            raise ValueError(msg.format(subtype=subtype, other=key_dtype))

        return key_i8
