    @Appender(ops.make_flex_doc("rmod", "dataframe"))
    def rmod(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, roperator.rmod, level=level, fill_value=fill_value, axis=axis
        )
