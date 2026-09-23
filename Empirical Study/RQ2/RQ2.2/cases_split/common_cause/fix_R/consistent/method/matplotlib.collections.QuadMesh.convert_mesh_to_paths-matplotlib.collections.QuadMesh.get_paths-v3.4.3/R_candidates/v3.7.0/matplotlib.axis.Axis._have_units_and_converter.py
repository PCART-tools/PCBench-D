    def _have_units_and_converter(self):
        """
        Return `True` if units and a converter have been set.
        """
        return self.converter is not None and self.units is not None
