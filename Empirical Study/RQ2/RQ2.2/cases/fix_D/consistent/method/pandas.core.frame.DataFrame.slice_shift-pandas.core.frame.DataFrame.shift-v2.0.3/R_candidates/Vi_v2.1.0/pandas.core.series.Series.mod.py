    @Appender(ops.make_flex_doc("mod", "series"))
    def mod(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, operator.mod, level=level, fill_value=fill_value, axis=axis
        )
