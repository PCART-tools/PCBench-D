    def get_dashes(self):
        """
        Return the dash information as an offset dashlist tuple.

        The dash list is a even size list that gives the ink on, ink
        off in pixels.

        See p107 of to PostScript `BLUEBOOK
        <https://www-cdf.fnal.gov/offline/PostScript/BLUEBOOK.PDF>`_
        for more info.

        Default value is None
        """
        return self._dashes
