    def set_edgecolor(self, c):
        """
        Set the edgecolor(s) of the collection. *c* can be a
        matplotlib color spec (all patches have same color), or a
        sequence of specs; if it is a sequence the patches will
        cycle through the sequence.

        If *c* is 'face', the edge color will always be the same as
        the face color.  If it is 'none', the patch boundary will not
        be drawn.

        ACCEPTS: matplotlib color spec or sequence of specs
        """
        self._original_edgecolor = c
        self._set_edgecolor(c)
