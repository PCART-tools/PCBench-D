    def set_position(self, pos, which='both'):
        """Set the axes position

        The expected shape of ``pos`` is::

          pos = [left, bottom, width, height]

        in relative 0,1 coords, or *pos* can be a
        :class:`~matplotlib.transforms.Bbox`

        There are two position variables: one which is ultimately
        used, but which may be modified by :meth:`apply_aspect`, and a
        second which is the starting point for :meth:`apply_aspect`.


        Optional keyword arguments:
          *which*

            ==========   ====================
            value        description
            ==========   ====================
            'active'     to change the first
            'original'   to change the second
            'both'       to change both
            ==========   ====================

        """
        if not isinstance(pos, mtransforms.BboxBase):
            pos = mtransforms.Bbox.from_bounds(*pos)
        if which in ('both', 'active'):
            self._position.set(pos)
        if which in ('both', 'original'):
            self._originalPosition.set(pos)
        self.stale = True
