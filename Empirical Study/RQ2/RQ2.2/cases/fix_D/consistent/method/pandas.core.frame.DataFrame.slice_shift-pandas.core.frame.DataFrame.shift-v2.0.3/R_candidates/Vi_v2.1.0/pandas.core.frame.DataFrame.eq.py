    @Appender(ops.make_flex_doc("eq", "dataframe"))
    def eq(self, other, axis: Axis = "columns", level=None):
        return self._flex_cmp_method(other, operator.eq, axis=axis, level=level)
