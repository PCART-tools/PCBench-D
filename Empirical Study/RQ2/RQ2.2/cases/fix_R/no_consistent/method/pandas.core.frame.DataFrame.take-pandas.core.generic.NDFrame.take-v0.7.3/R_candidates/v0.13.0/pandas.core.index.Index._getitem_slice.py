    def _getitem_slice(self, key):
        """ getitem for a bool/sliceable, fallback to standard getitem """
        try:
            arr_idx = self.view(np.ndarray)
            result = arr_idx[key]
            return self.__class__(result, name=self.name, fastpath=True)
        except:
            return self.__getitem__(key)
