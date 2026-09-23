    def gradient(self, x, y):
        return self._interpolate_multikeys(x, y, tri_index=None,
                                           return_keys=('dzdx', 'dzdy'))
