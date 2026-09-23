    def set_color(self, c):
        """
        Set the edgecolor.

        Parameters
        ----------
        c : color or sequence of rgba tuples

        .. seealso::

            :meth:`set_facecolor`, :meth:`set_edgecolor`
               For setting the edge or face color individually.
        """
        # The facecolor of a spine is always 'none' by default -- let
        # the user change it manually if desired.
        self.set_edgecolor(c)
        self.stale = True
