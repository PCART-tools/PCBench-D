    @Appender(ops.make_flex_doc("ge", "dataframe"))
    def ge(self, other, axis: Axis = "columns", level=None):
        return self._flex_cmp_method(other, operator.ge, axis=axis, level=level)
