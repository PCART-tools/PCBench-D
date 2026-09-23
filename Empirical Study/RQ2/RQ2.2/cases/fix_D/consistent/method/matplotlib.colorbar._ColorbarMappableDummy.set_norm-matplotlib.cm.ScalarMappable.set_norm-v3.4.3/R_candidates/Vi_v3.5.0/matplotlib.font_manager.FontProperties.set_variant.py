    def set_variant(self, variant):
        """
        Set the font variant.  Values are: 'normal' or 'small-caps'.
        """
        if variant is None:
            variant = rcParams['font.variant']
        _api.check_in_list(['normal', 'small-caps'], variant=variant)
        self._variant = variant
