    def _format_native_types(
        self, na_rep="", float_format=None, decimal=".", quoting=None, **kwargs
    ):
        from pandas.io.formats.format import FloatArrayFormatter

        if is_float_dtype(self.dtype):
            formatter = FloatArrayFormatter(
                self._values,
                na_rep=na_rep,
                float_format=float_format,
                decimal=decimal,
                quoting=quoting,
                fixed_width=False,
            )
            return formatter.get_result_as_array()

        return super()._format_native_types(
            na_rep=na_rep,
            float_format=float_format,
            decimal=decimal,
            quoting=quoting,
            **kwargs,
        )
