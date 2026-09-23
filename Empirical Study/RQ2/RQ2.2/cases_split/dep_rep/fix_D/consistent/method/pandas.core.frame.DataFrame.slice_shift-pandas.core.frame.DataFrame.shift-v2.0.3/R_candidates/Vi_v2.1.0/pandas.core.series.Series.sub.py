    @Appender(ops.make_flex_doc("sub", "series"))
    def sub(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.sub, level=level, fill_value=fill_value, axis=axis
        )
