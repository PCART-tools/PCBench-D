    @property
    def colspan(self):
        """The columns spanned by this subplot, as a `range` object."""
        ncols = self.get_gridspec().ncols
        # We explicitly support num2 refering to a column on num1's *left*, so
        # we must sort the column indices here so that the range makes sense.
        c1, c2 = sorted([self.num1 % ncols, self.num2 % ncols])
        return range(c1, c2 + 1)
