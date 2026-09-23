    @Appender(ops.make_flex_doc("gt", "series"))
    def gt(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.gt, level=level, fill_value=fill_value, axis=axis
        )
