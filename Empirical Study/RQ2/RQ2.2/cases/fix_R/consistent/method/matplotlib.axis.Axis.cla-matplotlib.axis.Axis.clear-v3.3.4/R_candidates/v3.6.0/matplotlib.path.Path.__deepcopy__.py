    def __deepcopy__(self, memo=None):
        """
        Return a deepcopy of the `Path`.  The `Path` will not be
        readonly, even if the source `Path` is.
        """
        # Deepcopying arrays (vertices, codes) strips the writeable=False flag.
        p = copy.deepcopy(super(), memo)
        p._readonly = False
        return p
