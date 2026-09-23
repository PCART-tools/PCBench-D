    @doc(ExtensionArray.to_numpy)
    def to_numpy(
        self,
        dtype: npt.DTypeLike | None = None,
        copy: bool = False,
        na_value: object = lib.no_default,
    ) -> np.ndarray:
        if dtype is not None:
            dtype = np.dtype(dtype)
        elif self._hasna:
            dtype = np.dtype(object)

        if na_value is lib.no_default:
            na_value = self.dtype.na_value

        pa_type = self._pa_array.type
        if pa.types.is_timestamp(pa_type) or pa.types.is_duration(pa_type):
            result = self._maybe_convert_datelike_array()
            if dtype is None or dtype.kind == "O":
                result = result.to_numpy(dtype=object, na_value=na_value)
            else:
                result = result.to_numpy(dtype=dtype)
            return result
        elif pa.types.is_time(pa_type) or pa.types.is_date(pa_type):
            # convert to list of python datetime.time objects before
            # wrapping in ndarray
            result = np.array(list(self), dtype=dtype)
        elif is_object_dtype(dtype) and self._hasna:
            result = np.empty(len(self), dtype=object)
            mask = ~self.isna()
            result[mask] = np.asarray(self[mask]._pa_array)
        elif pa.types.is_null(self._pa_array.type):
            fill_value = None if isna(na_value) else na_value
            return np.full(len(self), fill_value=fill_value, dtype=dtype)
        elif self._hasna:
            data = self.fillna(na_value)
            result = data._pa_array.to_numpy()
            if dtype is not None:
                result = result.astype(dtype, copy=False)
            return result
        else:
            result = self._pa_array.to_numpy()
            if dtype is not None:
                result = result.astype(dtype, copy=False)
            if copy:
                result = result.copy()
            return result
        if self._hasna:
            result[self.isna()] = na_value
        return result
