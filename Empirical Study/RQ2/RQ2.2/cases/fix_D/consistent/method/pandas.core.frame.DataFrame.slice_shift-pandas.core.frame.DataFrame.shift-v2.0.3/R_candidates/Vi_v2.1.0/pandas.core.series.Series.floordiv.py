    @Appender(ops.make_flex_doc("floordiv", "series"))
    def floordiv(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.floordiv, level=level, fill_value=fill_value, axis=axis
        )
