    def set_axisbelow(self, b):
        """
        Set whether the axis ticks and gridlines are above or below most
        artists

        ACCEPTS: [ *True* | *False* | 'line' ]
        """
        self._axisbelow = validate_axisbelow(b)
        self.stale = True
