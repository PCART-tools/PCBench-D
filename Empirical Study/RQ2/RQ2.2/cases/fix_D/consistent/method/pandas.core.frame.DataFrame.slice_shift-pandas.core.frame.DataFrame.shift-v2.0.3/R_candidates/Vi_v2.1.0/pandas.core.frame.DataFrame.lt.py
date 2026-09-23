    @Appender(ops.make_flex_doc("lt", "dataframe"))
    def lt(self, other, axis: Axis = "columns", level=None):
        return self._flex_cmp_method(other, operator.lt, axis=axis, level=level)
