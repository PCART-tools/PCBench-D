    @Appender(ops.make_flex_doc("floordiv", "dataframe"))
    def floordiv(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, operator.floordiv, level=level, fill_value=fill_value, axis=axis
        )
