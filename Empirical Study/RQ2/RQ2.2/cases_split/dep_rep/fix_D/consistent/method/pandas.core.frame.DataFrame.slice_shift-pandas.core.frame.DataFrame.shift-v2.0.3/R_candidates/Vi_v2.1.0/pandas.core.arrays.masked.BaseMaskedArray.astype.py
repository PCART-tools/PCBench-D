    def astype(self, dtype: AstypeArg, copy: bool = True) -> ArrayLike:
        dtype = pandas_dtype(dtype)

        if dtype == self.dtype:
            if copy:
                return self.copy()
            return self

        # if we are astyping to another nullable masked dtype, we can fastpath
        if isinstance(dtype, BaseMaskedDtype):
            # TODO deal with NaNs for FloatingArray case
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RuntimeWarning)
                # TODO: Is rounding what we want long term?
                data = self._data.astype(dtype.numpy_dtype, copy=copy)
            # mask is copied depending on whether the data was copied, and
            # not directly depending on the `copy` keyword
            mask = self._mask if data is self._data else self._mask.copy()
            cls = dtype.construct_array_type()
            return cls(data, mask, copy=False)

        if isinstance(dtype, ExtensionDtype):
            eacls = dtype.construct_array_type()
            return eacls._from_sequence(self, dtype=dtype, copy=copy)

        na_value: float | np.datetime64 | lib.NoDefault

        # coerce
        if dtype.kind == "f":
            # In astype, we consider dtype=float to also mean na_value=np.nan
            na_value = np.nan
        elif dtype.kind == "M":
            na_value = np.datetime64("NaT")
        else:
            na_value = lib.no_default

        # to_numpy will also raise, but we get somewhat nicer exception messages here
        if dtype.kind in "iu" and self._hasna:
            raise ValueError("cannot convert NA to integer")
        if dtype.kind == "b" and self._hasna:
            # careful: astype_nansafe converts np.nan to True
            raise ValueError("cannot convert float NaN to bool")

        data = self.to_numpy(dtype=dtype, na_value=na_value, copy=copy)
        return data
