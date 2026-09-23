    @Appender(ops.make_flex_doc("rfloordiv", "series"))
    def rfloordiv(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, roperator.rfloordiv, level=level, fill_value=fill_value, axis=axis
        )
