    def get_in_layout(self):
        """
        Return boolean flag, ``True`` if artist is included in layout
        calculations.

        E.g. :ref:`constrainedlayout_guide`,
        `.Figure.tight_layout()`, and
        ``fig.savefig(fname, bbox_inches='tight')``.
        """
        return self._in_layout
