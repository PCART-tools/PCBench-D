    def _combine(self, other, func, axis=0):
        if isinstance(other, Panel):
            return self._combine_panel(other, func)
        elif isinstance(other, DataFrame):
            return self._combine_frame(other, func, axis=axis)
        elif is_scalar(other):
            return self._combine_const(other, func)
        else:
            raise NotImplementedError("%s is not supported in combine "
                                      "operation with %s" %
                                      (str(type(other)), str(type(self))))
