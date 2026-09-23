    def transform(self, effects):
        """
        Transform the font by slanting or extending. *effects* should
        be a dict where ``effects['slant']`` is the tangent of the
        angle that the font is to be slanted to the right (so negative
        values slant to the left) and ``effects['extend']`` is the
        multiplier by which the font is to be extended (so values less
        than 1.0 condense). Returns a new :class:`Type1Font` object.
        """
        with io.BytesIO() as buffer:
            tokenizer = self._tokens(self.parts[0])
            transformed =  self._transformer(tokenizer,
                                             slant=effects.get('slant', 0.0),
                                             extend=effects.get('extend', 1.0))
            list(map(buffer.write, transformed))
            return Type1Font((buffer.getvalue(), self.parts[1], self.parts[2]))
