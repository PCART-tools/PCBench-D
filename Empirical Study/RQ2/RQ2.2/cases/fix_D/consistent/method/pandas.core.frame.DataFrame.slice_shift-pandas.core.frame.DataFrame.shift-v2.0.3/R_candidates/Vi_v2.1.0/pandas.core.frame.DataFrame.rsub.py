    @Appender(ops.make_flex_doc("rsub", "dataframe"))
    def rsub(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, roperator.rsub, level=level, fill_value=fill_value, axis=axis
        )
