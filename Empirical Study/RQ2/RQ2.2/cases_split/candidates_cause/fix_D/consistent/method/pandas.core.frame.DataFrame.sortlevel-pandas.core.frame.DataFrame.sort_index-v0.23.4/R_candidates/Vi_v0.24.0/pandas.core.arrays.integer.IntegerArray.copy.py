    def copy(self, deep=False):
        data, mask = self._data, self._mask
        if deep:
            data = copy.deepcopy(data)
            mask = copy.deepcopy(mask)
        else:
            data = data.copy()
            mask = mask.copy()
        return type(self)(data, mask, copy=False)
