    def _get_value(self, *args, **kwargs):
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

        return lower._get_value(*args[1:], takeable=takeable)
