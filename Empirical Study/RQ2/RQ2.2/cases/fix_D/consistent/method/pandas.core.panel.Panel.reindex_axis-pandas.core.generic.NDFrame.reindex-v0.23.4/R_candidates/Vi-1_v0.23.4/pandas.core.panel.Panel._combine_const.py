    def _combine_const(self, other, func, try_cast=True):
        with np.errstate(all='ignore'):
            new_values = func(self.values, other)
        d = self._construct_axes_dict()
        return self._constructor(new_values, **d)
