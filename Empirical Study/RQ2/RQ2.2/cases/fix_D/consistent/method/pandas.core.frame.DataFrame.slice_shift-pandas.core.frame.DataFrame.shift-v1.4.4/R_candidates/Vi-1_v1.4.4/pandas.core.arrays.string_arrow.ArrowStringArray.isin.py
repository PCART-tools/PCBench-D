    def isin(self, values):
        if pa_version_under2p0:
            return super().isin(values)

        value_set = [
            pa_scalar.as_py()
            for pa_scalar in [pa.scalar(value, from_pandas=True) for value in values]
            if pa_scalar.type in (pa.string(), pa.null())
        ]

        # for an empty value_set pyarrow 3.0.0 segfaults and pyarrow 2.0.0 returns True
        # for null values, so we short-circuit to return all False array.
        if not len(value_set):
            return np.zeros(len(self), dtype=bool)

        kwargs = {}
        if pa_version_under3p0:
            # in pyarrow 2.0.0 skip_null is ignored but is a required keyword and raises
            # with unexpected keyword argument in pyarrow 3.0.0+
            kwargs["skip_null"] = True

        result = pc.is_in(self._data, value_set=pa.array(value_set), **kwargs)
        # pyarrow 2.0.0 returned nulls, so we explicily specify dtype to convert nulls
        # to False
        return np.array(result, dtype=np.bool_)
