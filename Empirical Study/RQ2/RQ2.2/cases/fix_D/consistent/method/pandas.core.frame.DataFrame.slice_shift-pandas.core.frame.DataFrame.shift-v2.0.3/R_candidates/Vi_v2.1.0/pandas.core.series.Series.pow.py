    @Appender(ops.make_flex_doc("pow", "series"))
    def pow(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.pow, level=level, fill_value=fill_value, axis=axis
        )
