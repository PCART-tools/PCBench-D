    @Appender(ops.make_flex_doc("rmul", "series"))
    def rmul(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, roperator.rmul, level=level, fill_value=fill_value, axis=axis
        )
