    def get_unitless_position(self):
        "Return the unitless position of the text as a tuple (*x*, *y*)"
        # This will get the position with all unit information stripped away.
        # This is here for convenience since it is done in several locations.
        x = float(self.convert_xunits(self._x))
        y = float(self.convert_yunits(self._y))
        return x, y
