    @Appender(ops.make_flex_doc("rmul", "dataframe"))
    def rmul(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, roperator.rmul, level=level, fill_value=fill_value, axis=axis
        )
