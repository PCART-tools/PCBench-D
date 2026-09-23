    @Appender(ops.make_flex_doc("truediv", "dataframe"))
    def truediv(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, operator.truediv, level=level, fill_value=fill_value, axis=axis
        )
