    def set_fontvariant(self, variant):
        """
        Set the font variant, either 'normal' or 'small-caps'.

        Parameters
        ----------
        variant : {'normal', 'small-caps'}

        See Also
        --------
        .font_manager.FontProperties.set_variant
        """
        self._fontproperties.set_variant(variant)
        self.stale = True
