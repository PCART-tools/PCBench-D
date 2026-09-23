    def inverted(self):
        """
        Return the corresponding inverse transformation.

        The return value of this method should be treated as
        temporary.  An update to *self* does not cause a corresponding
        update to its inverted copy.

        ``x === self.inverted().transform(self.transform(x))``
        """
        raise NotImplementedError()
