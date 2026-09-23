    def __init__(self, value, units):
        """
        Create a new UnitDbl object.

        Units are internally converted to km, rad, and sec.  The only
        valid inputs for units are [m, km, mile, rad, deg, sec, min, hour].

        The field UnitDbl.value will contain the converted value.  Use
        the convert() method to get a specific type of units back.

        = ERROR CONDITIONS
        - If the input units are not in the allowed list, an error is thrown.

        = INPUT VARIABLES
        - value     The numeric value of the UnitDbl.
        - units     The string name of the units the value is in.
        """
        data = _api.check_getitem(self.allowed, units=units)
        self._value = float(value * data[0])
        self._units = data[1]
