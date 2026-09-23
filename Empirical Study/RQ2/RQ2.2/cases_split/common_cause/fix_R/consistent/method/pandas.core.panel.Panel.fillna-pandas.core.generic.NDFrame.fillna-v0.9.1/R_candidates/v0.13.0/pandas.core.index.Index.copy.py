    def copy(self, names=None, name=None, dtype=None, deep=False):
        """
        Make a copy of this object.  Name and dtype sets those attributes on
        the new object.

        Parameters
        ----------
        name : string, optional
        dtype : numpy dtype or pandas type

        Returns
        -------
        copy : Index

        Notes
        -----
        In most cases, there should be no functional difference from using
        ``deep``, but if ``deep`` is passed it will attempt to deepcopy.
        """
        if names is not None and name is not None:
            raise TypeError("Can only provide one of `names` and `name`")
        if deep:
            from copy import deepcopy
            new_index = np.ndarray.__deepcopy__(self, {}).view(self.__class__)
            name = name or deepcopy(self.name)
        else:
            new_index = super(Index, self).copy()
        if name is not None:
            names = [name]
        if names:
            new_index = new_index.set_names(names)
        if dtype:
            new_index = new_index.astype(dtype)
        return new_index
