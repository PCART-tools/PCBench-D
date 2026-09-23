    @Appender(ops.make_flex_doc("rtruediv", "series"))
    def rtruediv(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, roperator.rtruediv, level=level, fill_value=fill_value, axis=axis
        )
