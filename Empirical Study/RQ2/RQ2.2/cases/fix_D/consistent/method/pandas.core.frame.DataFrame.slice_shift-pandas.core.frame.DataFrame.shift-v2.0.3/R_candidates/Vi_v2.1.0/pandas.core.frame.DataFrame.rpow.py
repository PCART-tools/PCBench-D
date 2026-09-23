    @Appender(ops.make_flex_doc("rpow", "dataframe"))
    def rpow(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, roperator.rpow, level=level, fill_value=fill_value, axis=axis
        )
