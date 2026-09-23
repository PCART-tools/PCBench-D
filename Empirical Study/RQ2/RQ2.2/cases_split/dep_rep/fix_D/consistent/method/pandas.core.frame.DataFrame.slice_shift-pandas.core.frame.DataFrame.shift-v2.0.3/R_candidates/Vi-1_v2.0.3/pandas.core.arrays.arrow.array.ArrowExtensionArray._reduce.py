    def _reduce(self, name: str, *, skipna: bool = True, **kwargs):
        """
        Return a scalar result of performing the reduction operation.

        Parameters
        ----------
        name : str
            Name of the function, supported values are:
            { any, all, min, max, sum, mean, median, prod,
            std, var, sem, kurt, skew }.
        skipna : bool, default True
            If True, skip NaN values.
        **kwargs
            Additional keyword arguments passed to the reduction function.
            Currently, `ddof` is the only supported kwarg.

        Returns
        -------
        scalar

        Raises
        ------
        TypeError : subclass does not define reductions
        """
        pa_type = self._data.type

        data_to_reduce = self._data

        if name in ["any", "all"] and (
            pa.types.is_integer(pa_type)
            or pa.types.is_floating(pa_type)
            or pa.types.is_duration(pa_type)
            or pa.types.is_decimal(pa_type)
        ):
            # pyarrow only supports any/all for boolean dtype, we allow
            #  for other dtypes, matching our non-pyarrow behavior

            if pa.types.is_duration(pa_type):
                data_to_cmp = self._data.cast(pa.int64())
            else:
                data_to_cmp = self._data

            not_eq = pc.not_equal(data_to_cmp, 0)
            data_to_reduce = not_eq

        elif name in ["min", "max", "sum"] and pa.types.is_duration(pa_type):
            data_to_reduce = self._data.cast(pa.int64())

        elif name in ["median", "mean", "std", "sem"] and pa.types.is_temporal(pa_type):
            nbits = pa_type.bit_width
            if nbits == 32:
                data_to_reduce = self._data.cast(pa.int32())
            else:
                data_to_reduce = self._data.cast(pa.int64())

        if name == "sem":

            def pyarrow_meth(data, skip_nulls, **kwargs):
                numerator = pc.stddev(data, skip_nulls=skip_nulls, **kwargs)
                denominator = pc.sqrt_checked(pc.count(self._data))
                return pc.divide_checked(numerator, denominator)

        else:
            pyarrow_name = {
                "median": "quantile",
                "prod": "product",
                "std": "stddev",
                "var": "variance",
            }.get(name, name)
            # error: Incompatible types in assignment
            # (expression has type "Optional[Any]", variable has type
            # "Callable[[Any, Any, KwArg(Any)], Any]")
            pyarrow_meth = getattr(pc, pyarrow_name, None)  # type: ignore[assignment]
            if pyarrow_meth is None:
                # Let ExtensionArray._reduce raise the TypeError
                return super()._reduce(name, skipna=skipna, **kwargs)

        # GH51624: pyarrow defaults to min_count=1, pandas behavior is min_count=0
        if name in ["any", "all"] and "min_count" not in kwargs:
            kwargs["min_count"] = 0
        elif name == "median":
            # GH 52679: Use quantile instead of approximate_median
            kwargs["q"] = 0.5

        try:
            result = pyarrow_meth(data_to_reduce, skip_nulls=skipna, **kwargs)
        except (AttributeError, NotImplementedError, TypeError) as err:
            msg = (
                f"'{type(self).__name__}' with dtype {self.dtype} "
                f"does not support reduction '{name}' with pyarrow "
                f"version {pa.__version__}. '{name}' may be supported by "
                f"upgrading pyarrow."
            )
            raise TypeError(msg) from err
        if name == "median":
            # GH 52679: Use quantile instead of approximate_median; returns array
            result = result[0]
        if pc.is_null(result).as_py():
            return self.dtype.na_value

        if name in ["min", "max", "sum"] and pa.types.is_duration(pa_type):
            result = result.cast(pa_type)
        if name in ["median", "mean"] and pa.types.is_temporal(pa_type):
            result = result.cast(pa_type)
        if name in ["std", "sem"] and pa.types.is_temporal(pa_type):
            result = result.cast(pa.int64())
            if pa.types.is_duration(pa_type):
                result = result.cast(pa_type)
            elif pa.types.is_time(pa_type):
                unit = get_unit_from_pa_dtype(pa_type)
                result = result.cast(pa.duration(unit))
            elif pa.types.is_date(pa_type):
                # go with closest available unit, i.e. "s"
                result = result.cast(pa.duration("s"))
            else:
                # i.e. timestamp
                result = result.cast(pa.duration(pa_type.unit))

        return result.as_py()
