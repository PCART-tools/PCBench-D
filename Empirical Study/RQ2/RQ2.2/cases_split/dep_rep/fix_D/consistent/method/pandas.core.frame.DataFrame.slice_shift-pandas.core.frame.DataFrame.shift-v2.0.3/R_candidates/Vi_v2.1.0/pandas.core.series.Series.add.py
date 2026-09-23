    @Appender(ops.make_flex_doc("add", "series"))
    def add(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.add, level=level, fill_value=fill_value, axis=axis
        )
