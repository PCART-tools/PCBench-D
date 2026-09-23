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
            for arg in inputs:
                if isinstance(arg, (int, float, np.ndarray)):
                    args.append(arg)
                elif isinstance(arg, Series):
                    args.append(arg.to_physical()._s.to_numpy_view())
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

            # Only generalized ufuncs have a signature set:
            is_generalized_ufunc = bool(ufunc.signature)

            if is_generalized_ufunc:
                # Generalized ufuncs will operate on the whole array, so
                # missing data can corrupt the results.
                if self.has_nulls():
                    msg = "Can't pass a Series with missing data to a generalized ufunc, as it might give unexpected results. See https://docs.pola.rs/user-guide/expressions/missing-data/ for suggestions on how to remove or fill in missing data."
                    raise ComputeError(msg)
                # If the input and output are the same size, e.g. "(n)->(n)" we
                # can allocate ourselves and save a copy. If they're different,
                # we let the ufunc do the allocation, since only it knows the
                # output size.
                assert ufunc.signature is not None  # pacify MyPy
                ufunc_input, ufunc_output = ufunc.signature.split("->")
                if ufunc_output == "()":
                    # If the result a scalar, just let the function do its
                    # thing, no need for any song and dance involving
                    # allocation:
                    return ufunc(*args, dtype=dtype_char, **kwargs)
                else:
                    allocate_output = ufunc_input == ufunc_output
            else:
                allocate_output = True

            f = get_ffi_func("apply_ufunc_<>", numpy_char_code_to_dtype(dtype_char), s)

            if f is None:
                msg = (
                    "could not find "
                    f"`apply_ufunc_{numpy_char_code_to_dtype(dtype_char)}`"
                )
                raise NotImplementedError(msg)

            series = f(
                lambda out: ufunc(*args, out=out, dtype=dtype_char, **kwargs),
                allocate_output,
            )

            result = self._from_pyseries(series)
            if is_generalized_ufunc:
                # In this case we've disallowed passing in missing data, so no
                # further processing is needed.
                return result

            # We're using a regular ufunc, that operates value by value. That
            # means we allowed missing data in the input, so filter it out:
            validity_mask = self.is_not_null()
            for arg in inputs:
                if isinstance(arg, Series):
                    validity_mask &= arg.is_not_null()
            return (
                result.to_frame()
                .select(F.when(validity_mask).then(F.col(self.name)))
                .to_series(0)
            )
        else:
            msg = (
                "only `__call__` is implemented for numpy ufuncs on a Series, got "
                f"`{method!r}`"
            )
            raise NotImplementedError(msg)
