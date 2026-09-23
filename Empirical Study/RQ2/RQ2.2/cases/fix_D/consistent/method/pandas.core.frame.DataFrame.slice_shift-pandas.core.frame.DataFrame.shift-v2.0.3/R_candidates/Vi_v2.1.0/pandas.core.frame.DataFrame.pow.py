    @Appender(ops.make_flex_doc("pow", "dataframe"))
    def pow(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, operator.pow, level=level, fill_value=fill_value, axis=axis
        )
