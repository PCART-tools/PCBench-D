    def update(self, data):
        """Maps new values to integer identifiers.

        Parameters
        ----------
        data: iterable
              sequence of string values

        Raises
        ------
        TypeError
              If the value in data is not a string, unicode, bytes type
        """
        data = np.atleast_1d(np.array(data, dtype=object))

        for val in OrderedDict.fromkeys(data):
            if not isinstance(val, (str, bytes)):
                raise TypeError("{val!r} is not a string".format(val=val))
            if val not in self._mapping:
                self._mapping[val] = next(self._counter)
