    @Appender(ops.make_flex_doc("rmod", "series"))
    def rmod(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, roperator.rmod, level=level, fill_value=fill_value, axis=axis
        )
