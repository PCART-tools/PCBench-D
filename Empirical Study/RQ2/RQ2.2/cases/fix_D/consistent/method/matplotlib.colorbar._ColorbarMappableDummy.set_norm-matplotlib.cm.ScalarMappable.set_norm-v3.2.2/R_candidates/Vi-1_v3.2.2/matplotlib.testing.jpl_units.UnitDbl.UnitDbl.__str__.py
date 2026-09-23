    def __str__(self):
        """Print the UnitDbl."""
        return "%g *%s" % (self._value, self._units)
