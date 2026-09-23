    @Appender(ops.make_flex_doc("truediv", "series"))
    def truediv(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.truediv, level=level, fill_value=fill_value, axis=axis
        )
