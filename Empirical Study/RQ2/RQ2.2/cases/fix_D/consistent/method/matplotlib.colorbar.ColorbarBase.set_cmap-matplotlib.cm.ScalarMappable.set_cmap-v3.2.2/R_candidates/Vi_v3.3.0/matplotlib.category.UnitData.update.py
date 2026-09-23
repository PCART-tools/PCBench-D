    def update(self, data):
        """
        Map new values to integer identifiers.

        Parameters
        ----------
        data : iterable of str or bytes

        Raises
        ------
        TypeError
            If elements in *data* are neither str nor bytes.
        """
        data = np.atleast_1d(np.array(data, dtype=object))
        # check if convertible to number:
        convertible = True
        for val in OrderedDict.fromkeys(data):
            # OrderedDict just iterates over unique values in data.
            cbook._check_isinstance((str, bytes), value=val)
            if convertible:
                # this will only be called so long as convertible is True.
                convertible = self._str_is_convertible(val)
            if val not in self._mapping:
                self._mapping[val] = next(self._counter)
        if convertible:
            _log.info('Using categorical units to plot a list of strings '
                      'that are all parsable as floats or dates. If these '
                      'strings should be plotted as numbers, cast to the '
                      'appropriate data type before plotting.')
