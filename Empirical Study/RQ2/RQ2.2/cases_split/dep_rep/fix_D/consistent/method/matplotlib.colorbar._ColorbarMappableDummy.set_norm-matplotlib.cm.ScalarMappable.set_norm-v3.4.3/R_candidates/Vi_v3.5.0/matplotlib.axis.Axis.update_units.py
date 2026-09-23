    def update_units(self, data):
        """
        Introspect *data* for units converter and update the
        axis.converter instance if necessary. Return *True*
        if *data* is registered for unit conversion.
        """
        converter = munits.registry.get_converter(data)
        if converter is None:
            return False

        neednew = self.converter != converter
        self.converter = converter
        default = self.converter.default_units(data, self)
        if default is not None and self.units is None:
            self.set_units(default)

        elif neednew:
            self._update_axisinfo()
        self.stale = True
        return True
