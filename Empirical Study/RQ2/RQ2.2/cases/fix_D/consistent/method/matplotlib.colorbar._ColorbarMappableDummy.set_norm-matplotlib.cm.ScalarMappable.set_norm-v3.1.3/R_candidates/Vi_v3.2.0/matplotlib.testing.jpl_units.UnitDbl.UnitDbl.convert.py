    def convert(self, units):
        """Convert the UnitDbl to a specific set of units.

        = ERROR CONDITIONS
        - If the input units are not in the allowed list, an error is thrown.

        = INPUT VARIABLES
        - units     The string name of the units to convert to.

        = RETURN VALUE
        - Returns the value of the UnitDbl in the requested units as a floating
          point number.
        """
        if self._units == units:
            return self._value
        data = cbook._check_getitem(self.allowed, units=units)
        if self._units != data[1]:
            raise ValueError(f"Error trying to convert to different units.\n"
                             f"    Invalid conversion requested.\n"
                             f"    UnitDbl: {self}\n"
                             f"    Units:   {units}\n")
        return self._value / data[0]
