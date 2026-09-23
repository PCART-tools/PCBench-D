    def __call__(self, x, pos=None):
        """
        Returns the label that matches the position regardless of the
        value.

        For positions ``pos < len(seq)``, return `seq[i]` regardless of
        `x`. Otherwise return empty string. `seq` is the sequence of
        strings that this object was initialized with.
        """
        if pos is None or pos >= len(self.seq):
            return ''
        else:
            return self.seq[pos]
