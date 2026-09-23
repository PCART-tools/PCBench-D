    def __array_ufunc__(
        self, ufunc: np.ufunc, method: str, *inputs: Any, **kwargs: Any
    ) -> Series:
        """Numpy universal functions."""
        if self._s.n_chunks() > 1:
            self._s.rechunk(in_place=True)

        s = self._s

        if method == "__call__":
            if ufunc.nout != 1:
                msg = "only ufuncs that return one 1D array are supported"
                raise NotImplementedError(msg)

            args: list[int | float | np.ndarray[Any, Any]] = []

            validity_mask = self.is_not_null()
            for arg in inputs:
                if isinstance(arg, (int, float, np.ndarray)):
                    args.append(arg)
                elif isinstance(arg, Series):
                    validity_mask &= arg.is_not_null()
                    args.append(arg._view(ignore_nulls=True))
                else:
                    msg = f"unsupported type {type(arg).__name__!r} for {arg!r}"
                    raise TypeError(msg)

            # Get minimum dtype needed to be able to cast all input arguments to the
            # same dtype.
            dtype_char_minimum = np.result_type(*args).char

            # Get all possible output dtypes for ufunc.
            # Input dtypes and output dtypes seem to always match for ufunc.types,
            # so pick all the different output dtypes.
            dtypes_ufunc = [
                input_output_type[-1]
                for input_output_type in ufunc.types
                if supported_numpy_char_code(input_output_type[-1])
            ]

            # Get the first ufunc dtype from all possible ufunc dtypes for which
            # the input arguments can be safely cast to that ufunc dtype.
            for dtype_ufunc in dtypes_ufunc:
                if np.can_cast(dtype_char_minimum, dtype_ufunc):
                    dtype_char_minimum = dtype_ufunc
                    break

            # Override minimum dtype if requested.
            dtype_char = (
                np.dtype(kwargs.pop("dtype")).char
                if "dtype" in kwargs
                else dtype_char_minimum
            )

            f = get_ffi_func("apply_ufunc_<>", numpy_char_code_to_dtype(dtype_char), s)

            if f is None:
                msg = (
                    "could not find "
                    f"`apply_ufunc_{numpy_char_code_to_dtype(dtype_char)}`"
                )
                raise NotImplementedError(msg)

            series = f(lambda out: ufunc(*args, out=out, dtype=dtype_char, **kwargs))
            return (
                self._from_pyseries(series)
                .to_frame()
                .select(F.when(validity_mask).then(F.col(self.name)))
                .to_series(0)
            )
        else:
            msg = (
                "only `__call__` is implemented for numpy ufuncs on a Series, got "
                f"`{method!r}`"
            )
            raise NotImplementedError(msg)
