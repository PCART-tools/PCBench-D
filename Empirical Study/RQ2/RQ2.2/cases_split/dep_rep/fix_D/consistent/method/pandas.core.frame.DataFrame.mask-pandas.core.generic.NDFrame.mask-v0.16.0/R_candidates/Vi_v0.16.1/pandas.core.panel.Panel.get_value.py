    def get_value(self, *args, **kwargs):
        """
        Quickly retrieve single value at (item, major, minor) location

        Parameters
        ----------
        item : item label (panel item)
        major : major axis label (panel item row)
        minor : minor axis label (panel item column)
        takeable : interpret the passed labels as indexers, default False

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
        takeable = kwargs.pop('takeable', None)

        if kwargs:
            raise TypeError('get_value() got an unexpected keyword '
                    'argument "{0}"'.format(list(kwargs.keys())[0]))

        if takeable is True:
            lower = self._iget_item_cache(args[0])
        else:
            lower = self._get_item_cache(args[0])

        return lower.get_value(*args[1:], takeable=takeable)
