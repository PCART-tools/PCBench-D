    def set_in_layout(self, in_layout):
        """
        Set if artist is to be included in layout calculations,
        E.g. :doc:`/tutorials/intermediate/constrainedlayout_guide`,
        `.Figure.tight_layout()`, and
        ``fig.savefig(fname, bbox_inches='tight')``.

        Parameters
        ----------
        in_layout : bool
        """
        self._in_layout = in_layout
