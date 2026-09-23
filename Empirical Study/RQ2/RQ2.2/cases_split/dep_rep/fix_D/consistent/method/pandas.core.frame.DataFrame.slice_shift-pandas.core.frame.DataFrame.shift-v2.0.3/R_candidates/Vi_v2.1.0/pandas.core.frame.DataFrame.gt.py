    @Appender(ops.make_flex_doc("gt", "dataframe"))
    def gt(self, other, axis: Axis = "columns", level=None):
        return self._flex_cmp_method(other, operator.gt, axis=axis, level=level)
