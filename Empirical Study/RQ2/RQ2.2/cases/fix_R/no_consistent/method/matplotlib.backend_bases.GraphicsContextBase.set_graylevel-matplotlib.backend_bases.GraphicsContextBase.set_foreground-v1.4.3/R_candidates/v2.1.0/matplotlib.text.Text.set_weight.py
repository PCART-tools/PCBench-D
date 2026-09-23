    def set_weight(self, weight):
        """
        Set the font weight.

        ACCEPTS: [a numeric value in range 0-1000 | 'ultralight' | 'light' |
                  'normal' | 'regular' | 'book' | 'medium' | 'roman' |
                  'semibold' | 'demibold' | 'demi' | 'bold' | 'heavy' |
                  'extra bold' | 'black' ]
        """
        self._fontproperties.set_weight(weight)
        self.stale = True
