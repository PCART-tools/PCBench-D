    @Appender(ops.make_flex_doc("mul", "dataframe"))
    def mul(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, operator.mul, level=level, fill_value=fill_value, axis=axis
        )
