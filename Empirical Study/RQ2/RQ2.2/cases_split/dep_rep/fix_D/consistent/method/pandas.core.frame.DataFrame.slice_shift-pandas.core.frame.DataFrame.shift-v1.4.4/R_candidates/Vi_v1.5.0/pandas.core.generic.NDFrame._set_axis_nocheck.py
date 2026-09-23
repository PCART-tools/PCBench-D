    @final
    def _set_axis_nocheck(self, labels, axis: Axis, inplace: bool_t, copy: bool_t):
        if inplace:
            setattr(self, self._get_axis_name(axis), labels)
        else:
            # With copy=False, we create a new object but don't copy the
            #  underlying data.
            obj = self.copy(deep=copy)
            setattr(obj, obj._get_axis_name(axis), labels)
            return obj
