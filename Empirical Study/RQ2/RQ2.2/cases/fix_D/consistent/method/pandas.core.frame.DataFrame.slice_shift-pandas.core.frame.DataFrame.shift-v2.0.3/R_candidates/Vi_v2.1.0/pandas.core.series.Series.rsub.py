    @Appender(ops.make_flex_doc("rsub", "series"))
    def rsub(self, other, level=None, fill_value=None, axis: Axis = 0):
        return self._flex_method(
            other, roperator.rsub, level=level, fill_value=fill_value, axis=axis
        )
