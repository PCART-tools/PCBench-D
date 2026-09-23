    def _wrap_array(self, arr, axes, copy=False):
        d = self._construct_axes_dict_from(self, axes, copy=copy)
        return self._constructor(arr, **d).__finalize__(self)
