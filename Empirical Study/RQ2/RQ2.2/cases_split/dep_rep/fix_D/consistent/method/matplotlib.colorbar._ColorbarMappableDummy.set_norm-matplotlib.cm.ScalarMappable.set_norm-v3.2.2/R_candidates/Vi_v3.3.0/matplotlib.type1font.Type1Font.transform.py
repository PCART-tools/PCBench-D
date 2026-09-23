    def transform(self, effects):
        """
        Return a new font that is slanted and/or extended.

        Parameters
        ----------
        effects : dict
            A dict with optional entries:

            - 'slant' : float, default: 0
                Tangent of the angle that the font is to be slanted to the
                right. Negative values slant to the left.
            - 'extend' : float, default: 1
                Scaling factor for the font width. Values less than 1 condense
                the glyphs.

        Returns
        -------
        `Type1Font`
        """
        tokenizer = self._tokens(self.parts[0])
        transformed = self._transformer(tokenizer,
                                        slant=effects.get('slant', 0.0),
                                        extend=effects.get('extend', 1.0))
        return Type1Font((b"".join(transformed), self.parts[1], self.parts[2]))
