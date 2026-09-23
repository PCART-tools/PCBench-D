    @Appender(ops.make_flex_doc("add", "dataframe"))
    def add(self, other, axis: Axis = "columns", level=None, fill_value=None):
        return self._flex_arith_method(
            other, operator.add, level=level, fill_value=fill_value, axis=axis
        )
