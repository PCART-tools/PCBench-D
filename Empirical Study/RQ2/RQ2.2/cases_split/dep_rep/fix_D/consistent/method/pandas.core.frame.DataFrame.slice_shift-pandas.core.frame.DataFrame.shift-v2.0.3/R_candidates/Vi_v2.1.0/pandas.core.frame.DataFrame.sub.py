    @Appender(ops.make_flex_doc("sub", "dataframe"))
    def sub(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, operator.sub, level=level, fill_value=fill_value, axis=axis
        )
