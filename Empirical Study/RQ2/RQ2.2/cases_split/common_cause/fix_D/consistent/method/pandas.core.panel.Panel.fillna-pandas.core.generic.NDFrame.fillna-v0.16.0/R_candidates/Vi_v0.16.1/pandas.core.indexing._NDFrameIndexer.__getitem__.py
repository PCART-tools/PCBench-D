    def __getitem__(self, key):
        if type(key) is tuple:
            try:
                values = self.obj.get_value(*key)
                if np.isscalar(values):
                    return values
            except Exception:
                pass

            return self._getitem_tuple(key)
        else:
            return self._getitem_axis(key, axis=0)
