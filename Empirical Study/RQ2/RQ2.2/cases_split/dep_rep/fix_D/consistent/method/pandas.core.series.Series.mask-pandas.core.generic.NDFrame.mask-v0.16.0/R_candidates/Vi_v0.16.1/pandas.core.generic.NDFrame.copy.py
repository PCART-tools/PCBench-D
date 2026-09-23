    def copy(self, deep=True):
        """
        Make a copy of this object

        Parameters
        ----------
        deep : boolean or string, default True
            Make a deep copy, i.e. also copy data

        Returns
        -------
        copy : type of caller
        """
        data = self._data.copy(deep=deep)
        return self._constructor(data).__finalize__(self)
