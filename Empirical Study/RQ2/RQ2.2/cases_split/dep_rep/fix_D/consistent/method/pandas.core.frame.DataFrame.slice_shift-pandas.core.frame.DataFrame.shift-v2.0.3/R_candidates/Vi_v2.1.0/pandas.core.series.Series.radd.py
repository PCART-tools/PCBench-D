    @Appender(ops.make_flex_doc("radd", "series"))
    def radd(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, roperator.radd, level=level, fill_value=fill_value, axis=axis
        )
