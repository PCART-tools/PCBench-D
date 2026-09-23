    @final
    def _set_axis_nocheck(self, labels, axis: Axis, inplace: bool_t):
        # NDFrame.rename with inplace=False calls set_axis(inplace=True) on a copy.
        if inplace:
            setattr(self, self._get_axis_name(axis), labels)
        else:
            obj = self.copy()
            obj.set_axis(labels, axis=axis, inplace=True)
            return obj
