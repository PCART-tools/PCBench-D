    def set_converter(self, converter):
        """
        Set the unit converter for axis.

        Parameters
        ----------
        converter : `~matplotlib.units.ConversionInterface`
        """
        self._set_converter(converter)
        self._converter_is_explicit = True
