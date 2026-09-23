    def set_stretch(self, stretch):
        """
        Set the font stretch (horizontal condensation or expansion).

        ACCEPTS: [a numeric value in range 0-1000 | 'ultra-condensed' |
                  'extra-condensed' | 'condensed' | 'semi-condensed' |
                  'normal' | 'semi-expanded' | 'expanded' | 'extra-expanded' |
                  'ultra-expanded' ]
        """
        self._fontproperties.set_stretch(stretch)
        self.stale = True
