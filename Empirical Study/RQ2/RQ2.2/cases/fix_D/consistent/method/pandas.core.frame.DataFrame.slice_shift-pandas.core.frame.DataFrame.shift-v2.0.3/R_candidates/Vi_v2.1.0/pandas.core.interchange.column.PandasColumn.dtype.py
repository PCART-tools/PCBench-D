    @cache_readonly
    def dtype(self) -> tuple[DtypeKind, int, str, str]:
        dtype = self._col.dtype

        if isinstance(dtype, pd.CategoricalDtype):
            codes = self._col.values.codes
            (
                _,
                bitwidth,
                c_arrow_dtype_f_str,
                _,
            ) = self._dtype_from_pandasdtype(codes.dtype)
            return (
                DtypeKind.CATEGORICAL,
                bitwidth,
                c_arrow_dtype_f_str,
                Endianness.NATIVE,
            )
        elif is_string_dtype(dtype):
            if infer_dtype(self._col) == "string":
                return (
                    DtypeKind.STRING,
                    8,
                    dtype_to_arrow_c_fmt(dtype),
                    Endianness.NATIVE,
                )
            raise NotImplementedError("Non-string object dtypes are not supported yet")
        else:
            return self._dtype_from_pandasdtype(dtype)
