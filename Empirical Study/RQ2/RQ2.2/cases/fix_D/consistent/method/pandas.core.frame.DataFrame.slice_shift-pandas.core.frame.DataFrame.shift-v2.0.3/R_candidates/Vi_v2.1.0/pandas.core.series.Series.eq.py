    @Appender(ops.make_flex_doc("eq", "series"))
    def eq(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.eq, level=level, fill_value=fill_value, axis=axis
        )
