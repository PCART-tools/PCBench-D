    def set_color(self, c):
        """
        Set both the edgecolor and the facecolor.

        .. seealso::

            :meth:`set_facecolor`, :meth:`set_edgecolor`
               For setting the edge or face color individually.

        Parameters
        ----------
        c : matplotlib color arg or sequence of rgba tuples
        """
        self.set_facecolor(c)
        self.set_edgecolor(c)
