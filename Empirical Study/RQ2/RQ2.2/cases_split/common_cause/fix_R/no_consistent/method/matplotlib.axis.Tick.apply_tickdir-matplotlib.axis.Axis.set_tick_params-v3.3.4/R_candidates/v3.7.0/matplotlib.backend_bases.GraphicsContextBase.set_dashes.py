    def set_dashes(self, dash_offset, dash_list):
        """
        Set the dash style for the gc.

        Parameters
        ----------
        dash_offset : float
            Distance, in points, into the dash pattern at which to
            start the pattern. It is usually set to 0.
        dash_list : array-like or None
            The on-off sequence as points.  None specifies a solid line. All
            values must otherwise be non-negative (:math:`\\ge 0`).

        Notes
        -----
        See p. 666 of the PostScript
        `Language Reference
        <https://www.adobe.com/jp/print/postscript/pdfs/PLRM.pdf>`_
        for more info.
        """
        if dash_list is not None:
            dl = np.asarray(dash_list)
            if np.any(dl < 0.0):
                raise ValueError(
                    "All values in the dash list must be non-negative")
            if dl.size and not np.any(dl > 0.0):
                raise ValueError(
                    'At least one value in the dash list must be positive')
        self._dashes = dash_offset, dash_list
