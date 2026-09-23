    @Appender(ops.make_flex_doc("le", "dataframe"))
    def le(self, other, axis: Axis = "columns", level=None):
        return self._flex_cmp_method(other, operator.le, axis=axis, level=level)
