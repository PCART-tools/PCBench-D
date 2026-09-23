    @Appender(ops.make_flex_doc("mod", "dataframe"))
    def mod(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, operator.mod, level=level, fill_value=fill_value, axis=axis
        )
