    @Appender(ops.make_flex_doc("lt", "series"))
    def lt(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.lt, level=level, fill_value=fill_value, axis=axis
        )
