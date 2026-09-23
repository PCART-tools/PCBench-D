    def _format_native_types(
        self,
        *,
        na_rep: str_t = "",
        decimal: str_t = ".",
        float_format=None,
        date_format=None,
        quoting=None,
    ) -> npt.NDArray[np.object_]:
        """
        Actually format specific types of the index.
        """
        from pandas.io.formats.format import FloatArrayFormatter

        if is_float_dtype(self.dtype) and not isinstance(self.dtype, ExtensionDtype):
            formatter = FloatArrayFormatter(
                self._values,
                na_rep=na_rep,
                float_format=float_format,
                decimal=decimal,
                quoting=quoting,
                fixed_width=False,
            )
            return formatter.get_result_as_array()

        mask = isna(self)
        if self.dtype != object and not quoting:
            values = np.asarray(self).astype(str)
        else:
            values = np.array(self, dtype=object, copy=True)

        values[mask] = na_rep
        return values
