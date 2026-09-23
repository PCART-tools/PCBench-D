    @Appender(ops.make_flex_doc("ge", "series"))
    def ge(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.ge, level=level, fill_value=fill_value, axis=axis
        )
