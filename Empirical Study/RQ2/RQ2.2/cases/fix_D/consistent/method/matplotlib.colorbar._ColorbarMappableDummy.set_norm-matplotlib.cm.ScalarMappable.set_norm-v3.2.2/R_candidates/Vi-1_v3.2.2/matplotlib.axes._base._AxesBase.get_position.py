    def get_position(self, original=False):
        """
        Get a copy of the axes rectangle as a `.Bbox`.

        Parameters
        ----------
        original : bool
            If ``True``, return the original position. Otherwise return the
            active position. For an explanation of the positions see
            `.set_position`.

        Returns
        -------
        pos : `.Bbox`

        """
        if original:
            return self._originalPosition.frozen()
        else:
            locator = self.get_axes_locator()
            if not locator:
                self.apply_aspect()
            return self._position.frozen()
