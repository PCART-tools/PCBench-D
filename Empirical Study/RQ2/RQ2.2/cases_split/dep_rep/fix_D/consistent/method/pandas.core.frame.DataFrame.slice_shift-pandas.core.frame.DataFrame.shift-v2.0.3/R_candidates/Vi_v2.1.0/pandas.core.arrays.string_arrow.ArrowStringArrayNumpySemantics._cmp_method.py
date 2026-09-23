    def _cmp_method(self, other, op):
        result = super()._cmp_method(other, op)
        return result.to_numpy(np.bool_, na_value=False)
