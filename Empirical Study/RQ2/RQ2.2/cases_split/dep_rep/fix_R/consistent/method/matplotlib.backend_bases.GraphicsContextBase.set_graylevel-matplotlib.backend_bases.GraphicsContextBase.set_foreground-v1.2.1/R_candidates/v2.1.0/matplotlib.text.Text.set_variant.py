    def set_variant(self, variant):
        """
        Set the font variant, either 'normal' or 'small-caps'.

        ACCEPTS: [ 'normal' | 'small-caps' ]
        """
        self._fontproperties.set_variant(variant)
        self.stale = True
