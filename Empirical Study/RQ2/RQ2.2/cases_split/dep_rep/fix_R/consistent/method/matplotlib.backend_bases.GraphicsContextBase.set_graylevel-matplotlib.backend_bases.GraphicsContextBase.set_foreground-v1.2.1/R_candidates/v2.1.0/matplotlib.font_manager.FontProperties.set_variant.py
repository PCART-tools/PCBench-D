    def set_variant(self, variant):
        """
        Set the font variant.  Values are: 'normal' or 'small-caps'.
        """
        if variant is None:
            variant = rcParams['font.variant']
        if variant not in ('normal', 'small-caps'):
            raise ValueError("variant must be normal or small-caps")
        self._variant = variant
