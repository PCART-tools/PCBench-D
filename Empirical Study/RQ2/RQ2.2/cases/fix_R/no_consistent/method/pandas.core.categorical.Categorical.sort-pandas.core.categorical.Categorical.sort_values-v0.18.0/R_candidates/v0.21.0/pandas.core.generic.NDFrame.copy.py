    def copy(self, deep=True):
        """
        Make a copy of this objects data.

        Parameters
        ----------
        deep : boolean or string, default True
            Make a deep copy, including a copy of the data and the indices.
            With ``deep=False`` neither the indices or the data are copied.

            Note that when ``deep=True`` data is copied, actual python objects
            will not be copied recursively, only the reference to the object.
            This is in contrast to ``copy.deepcopy`` in the Standard Library,
            which recursively copies object data.

        Returns
        -------
        copy : type of caller
        """
        data = self._data.copy(deep=deep)
        return self._constructor(data).__finalize__(self)
