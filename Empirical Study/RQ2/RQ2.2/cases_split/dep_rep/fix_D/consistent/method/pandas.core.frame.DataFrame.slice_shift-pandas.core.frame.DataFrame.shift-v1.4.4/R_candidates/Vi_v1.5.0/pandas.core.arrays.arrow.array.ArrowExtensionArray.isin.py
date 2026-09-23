    def isin(self, values) -> npt.NDArray[np.bool_]:
        if pa_version_under2p0:
            fallback_performancewarning(version="2")
            return super().isin(values)

        # for an empty value_set pyarrow 3.0.0 segfaults and pyarrow 2.0.0 returns True
        # for null values, so we short-circuit to return all False array.
        if not len(values):
            return np.zeros(len(self), dtype=bool)

        kwargs = {}
        if pa_version_under3p0:
            # in pyarrow 2.0.0 skip_null is ignored but is a required keyword and raises
            # with unexpected keyword argument in pyarrow 3.0.0+
            kwargs["skip_null"] = True

        result = pc.is_in(
            self._data, value_set=pa.array(values, from_pandas=True), **kwargs
        )
        # pyarrow 2.0.0 returned nulls, so we explicitly specify dtype to convert nulls
        # to False
        return np.array(result, dtype=np.bool_)
