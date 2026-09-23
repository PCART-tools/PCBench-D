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

        self.checkUnits(units)

        data = self.allowed[units]
        if self._units != data[1]:
            msg = "Error trying to convert to different units.\n" \
                    "    Invalid conversion requested.\n" \
                    "    UnitDbl: %s\n" \
                    "    Units:    %s\n" % (str(self), units)
            raise ValueError(msg)

        return self._value / data[0]
