    @Appender(ops.make_flex_doc("radd", "dataframe"))
    def radd(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, roperator.radd, level=level, fill_value=fill_value, axis=axis
        )
