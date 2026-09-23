    def add_suffix(self, suffix):
        """
        Concatenate suffix string with panel items names.

        Parameters
        ----------
        suffix : string

        Returns
        -------
        with_suffix : type of caller
        """
        new_data = self._data.add_suffix(suffix)
        return self._constructor(new_data).__finalize__(self)
