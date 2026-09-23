    def astype(self, dtype: AstypeArg, copy: bool = True) -> ArrayLike:
        """
        Cast to a NumPy array or ExtensionArray with 'dtype'.

        Parameters
        ----------
        dtype : str or dtype
            Typecode or data-type to which the array is cast.
        copy : bool, default True
            Whether to copy the data, even if not necessary. If False,
            a copy is made only if the old dtype does not match the
            new dtype.

        Returns
        -------
        ndarray or ExtensionArray
            NumPy ndarray, or BooleanArray, IntegerArray or FloatingArray with
            'dtype' for its dtype.

        Raises
        ------
        TypeError
            if incompatible type with an FloatingDtype, equivalent of same_kind
            casting
        """
        dtype = pandas_dtype(dtype)

        if isinstance(dtype, ExtensionDtype):
            return super().astype(dtype, copy=copy)

        # coerce
        if is_float_dtype(dtype):
            # In astype, we consider dtype=float to also mean na_value=np.nan
            kwargs = {"na_value": np.nan}
        elif is_datetime64_dtype(dtype):
            # error: Dict entry 0 has incompatible type "str": "datetime64"; expected
            # "str": "float"
            kwargs = {"na_value": np.datetime64("NaT")}  # type: ignore[dict-item]
        else:
            kwargs = {}

        # error: Argument 2 to "to_numpy" of "BaseMaskedArray" has incompatible
        # type "**Dict[str, float]"; expected "bool"
        data = self.to_numpy(dtype=dtype, **kwargs)  # type: ignore[arg-type]
        return astype_nansafe(data, dtype, copy=False)
