    def characteristic_function(self, t, **kwargs):
        """ Characteristic function """
        if not kwargs:
            cf = self._characteristic_function(t)
            if cf is not None:
                return cf
        return self.compute_characteristic_function(**kwargs)(t)
