    def set_color(self, c):
        """
        Set both the edgecolor and the facecolor.

        ACCEPTS: matplotlib color spec

        .. seealso::

            :meth:`set_facecolor`, :meth:`set_edgecolor`
               For setting the edge or face color individually.
        """
        self.set_facecolor(c)
        self.set_edgecolor(c)
