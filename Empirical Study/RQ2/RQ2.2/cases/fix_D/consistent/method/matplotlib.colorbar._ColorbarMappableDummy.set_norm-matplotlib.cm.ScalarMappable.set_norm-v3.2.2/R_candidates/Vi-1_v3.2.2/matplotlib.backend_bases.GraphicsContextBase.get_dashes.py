    def get_dashes(self):
        """
        Return the dash style as an (offset, dash-list) pair.

        The dash list is a even-length list that gives the ink on, ink off in
        points.  See p. 107 of to PostScript `blue book`_ for more info.

        Default value is (None, None).

        .. _blue book: https://www-cdf.fnal.gov/offline/PostScript/BLUEBOOK.PDF
        """
        return self._dashes
