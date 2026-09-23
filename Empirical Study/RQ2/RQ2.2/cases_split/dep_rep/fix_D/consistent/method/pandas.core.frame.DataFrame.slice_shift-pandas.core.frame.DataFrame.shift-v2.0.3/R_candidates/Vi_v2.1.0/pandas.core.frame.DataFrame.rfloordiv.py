    @Appender(ops.make_flex_doc("rfloordiv", "dataframe"))
    def rfloordiv(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, roperator.rfloordiv, level=level, fill_value=fill_value, axis=axis
        )
