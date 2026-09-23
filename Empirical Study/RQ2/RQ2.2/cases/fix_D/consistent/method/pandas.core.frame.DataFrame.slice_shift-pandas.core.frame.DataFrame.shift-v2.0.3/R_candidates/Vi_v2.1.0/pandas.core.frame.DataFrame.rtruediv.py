    @Appender(ops.make_flex_doc("rtruediv", "dataframe"))
    def rtruediv(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, roperator.rtruediv, level=level, fill_value=fill_value, axis=axis
        )
