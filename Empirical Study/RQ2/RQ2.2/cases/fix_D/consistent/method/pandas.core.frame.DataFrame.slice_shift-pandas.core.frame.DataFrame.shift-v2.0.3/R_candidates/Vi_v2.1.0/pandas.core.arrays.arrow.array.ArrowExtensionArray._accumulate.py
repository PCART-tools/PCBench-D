    def _accumulate(
        self, name: str, *, skipna: bool = True, **kwargs
    ) -> ArrowExtensionArray | ExtensionArray:
        """
        Return an ExtensionArray performing an accumulation operation.

        The underlying data type might change.

        Parameters
        ----------
        name : str
            Name of the function, supported values are:
            - cummin
            - cummax
            - cumsum
            - cumprod
        skipna : bool, default True
            If True, skip NA values.
        **kwargs
            Additional keyword arguments passed to the accumulation function.
            Currently, there is no supported kwarg.

        Returns
        -------
        array

        Raises
        ------
        NotImplementedError : subclass does not define accumulations
        """
        pyarrow_name = {
            "cummax": "cumulative_max",
            "cummin": "cumulative_min",
            "cumprod": "cumulative_prod_checked",
            "cumsum": "cumulative_sum_checked",
        }.get(name, name)
        pyarrow_meth = getattr(pc, pyarrow_name, None)
        if pyarrow_meth is None:
            return super()._accumulate(name, skipna=skipna, **kwargs)

        data_to_accum = self._pa_array

        pa_dtype = data_to_accum.type

        convert_to_int = (
            pa.types.is_temporal(pa_dtype) and name in ["cummax", "cummin"]
        ) or (pa.types.is_duration(pa_dtype) and name == "cumsum")

        if convert_to_int:
            if pa_dtype.bit_width == 32:
                data_to_accum = data_to_accum.cast(pa.int32())
            else:
                data_to_accum = data_to_accum.cast(pa.int64())

        result = pyarrow_meth(data_to_accum, skip_nulls=skipna, **kwargs)

        if convert_to_int:
            result = result.cast(pa_dtype)

        return type(self)(result)
