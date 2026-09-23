    def set_dashes(self, dash_offset, dash_list):
        """
        Set the dash style for the gc.

        Parameters
        ----------
        dash_offset : float or None
            The offset (usually 0).
        dash_list : array-like or None
            The on-off sequence as points.

        Notes
        -----
        ``(None, None)`` specifies a solid line.

        See p. 107 of to PostScript `blue book`_ for more info.

        .. _blue book: https://www-cdf.fnal.gov/offline/PostScript/BLUEBOOK.PDF
        """
        if dash_list is not None:
            dl = np.asarray(dash_list)
            if np.any(dl < 0.0):
                raise ValueError(
                    "All values in the dash list must be positive")
        self._dashes = dash_offset, dash_list
