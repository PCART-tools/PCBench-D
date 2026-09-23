    def convert_units(self, x):
        # If x is already a number, doesn't need converting
        if munits.ConversionInterface.is_numlike(x):
            return x

        if self.converter is None:
            self.converter = munits.registry.get_converter(x)

        if self.converter is None:
            return x

        ret = self.converter.convert(x, self.units, self)
        return ret
