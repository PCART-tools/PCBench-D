    def get_value(self, *args):
        """
        Quickly retrieve single value at (item, major, minor) location

        Parameters
        ----------
        item : item label (panel item)
        major : major axis label (panel item row)
        minor : minor axis label (panel item column)

        Returns
        -------
        value : scalar value
        """
        nargs = len(args)
        nreq = self._AXIS_LEN

        # require an arg for each axis
        if nargs != nreq:
            raise TypeError('There must be an argument for each axis, you gave'
                            ' {0} args, but {1} are required'.format(nargs,
                                                                     nreq))

        # hm, two layers to the onion
        frame = self._get_item_cache(args[0])
        return frame.get_value(*args[1:])
