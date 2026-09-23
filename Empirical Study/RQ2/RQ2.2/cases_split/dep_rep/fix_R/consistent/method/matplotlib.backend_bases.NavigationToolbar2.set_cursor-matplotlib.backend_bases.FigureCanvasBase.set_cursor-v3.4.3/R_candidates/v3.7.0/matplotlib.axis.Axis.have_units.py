    def have_units(self):
        """
        Return `True` if units or a converter have been set.
        """
        return self.converter is not None or self.units is not None
