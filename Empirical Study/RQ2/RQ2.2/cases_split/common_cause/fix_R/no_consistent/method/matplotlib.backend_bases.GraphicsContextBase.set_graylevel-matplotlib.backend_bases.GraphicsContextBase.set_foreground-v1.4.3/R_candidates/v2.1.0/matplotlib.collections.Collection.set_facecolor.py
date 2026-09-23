    def set_facecolor(self, c):
        """
        Set the facecolor(s) of the collection.  *c* can be a
        matplotlib color spec (all patches have same color), or a
        sequence of specs; if it is a sequence the patches will
        cycle through the sequence.

        If *c* is 'none', the patch will not be filled.

        ACCEPTS: matplotlib color spec or sequence of specs
        """
        self._original_facecolor = c
        self._set_facecolor(c)
