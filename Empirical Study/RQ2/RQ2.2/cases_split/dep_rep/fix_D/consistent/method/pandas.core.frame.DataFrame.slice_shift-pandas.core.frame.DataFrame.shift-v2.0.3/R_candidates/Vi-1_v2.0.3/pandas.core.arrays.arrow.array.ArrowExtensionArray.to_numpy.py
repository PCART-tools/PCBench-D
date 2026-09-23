    @doc(ExtensionArray.to_numpy)
    def to_numpy(
        self,
        dtype: npt.DTypeLike | None = None,
        copy: bool = False,
        na_value: object = lib.no_default,
    ) -> np.ndarray:
        if dtype is None and self._hasna:
            dtype = object
        if na_value is lib.no_default:
            na_value = self.dtype.na_value

        pa_type = self._data.type
        if pa.types.is_temporal(pa_type) and not pa.types.is_date(pa_type):
            # temporal types with units and/or timezones currently
            #  require pandas/python scalars to pass all tests
            # TODO: improve performance (this is slow)
            result = np.array(list(self), dtype=dtype)
        elif is_object_dtype(dtype) and self._hasna:
            result = np.empty(len(self), dtype=object)
            mask = ~self.isna()
            result[mask] = np.asarray(self[mask]._data)
        elif pa.types.is_null(self._data.type):
            result = np.asarray(self._data, dtype=dtype)
            if not isna(na_value):
                result[:] = na_value
            return result
        elif self._hasna:
            data = self.copy()
            data[self.isna()] = na_value
            return np.asarray(data._data, dtype=dtype)
        else:
            result = np.asarray(self._data, dtype=dtype)
            if copy:
                result = result.copy()
        if self._hasna:
            result[self.isna()] = na_value
        return result
