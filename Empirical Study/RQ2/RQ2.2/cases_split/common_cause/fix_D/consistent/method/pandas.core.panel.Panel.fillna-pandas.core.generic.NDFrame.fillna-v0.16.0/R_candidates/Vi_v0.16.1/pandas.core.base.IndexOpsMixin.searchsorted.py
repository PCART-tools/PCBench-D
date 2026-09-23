    def searchsorted(self, key, side='left'):
        """ np.ndarray searchsorted compat """

        ### FIXME in GH7447
        #### needs coercion on the key (DatetimeIndex does alreay)
        #### needs tests/doc-string
        return self.values.searchsorted(key, side=side)
