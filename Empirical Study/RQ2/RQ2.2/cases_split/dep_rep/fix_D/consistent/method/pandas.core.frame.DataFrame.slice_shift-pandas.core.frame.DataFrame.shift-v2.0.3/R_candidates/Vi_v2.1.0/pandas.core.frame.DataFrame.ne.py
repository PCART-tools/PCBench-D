    @Appender(ops.make_flex_doc("ne", "dataframe"))
    def ne(self, other, axis: Axis = "columns", level=None):
        return self._flex_cmp_method(other, operator.ne, axis=axis, level=level)
