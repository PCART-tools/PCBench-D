    def copy(self, names=None, dtype=None, levels=None, labels=None,
             deep=False):
        """
        Make a copy of this object. Names, dtype, levels and labels can be
        passed and will be set on new copy.

        Parameters
        ----------
        names : sequence, optional
        dtype : numpy dtype or pandas type, optional
        levels : sequence, optional
        labels : sequence, optional

        Returns
        -------
        copy : MultiIndex

        Notes
        -----
        In most cases, there should be no functional difference from using
        ``deep``, but if ``deep`` is passed it will attempt to deepcopy.
        This could be potentially expensive on large MultiIndex objects.
        """
        new_index = np.ndarray.copy(self)
        if deep:
            from copy import deepcopy
            levels = levels if levels is not None else deepcopy(self.levels)
            labels = labels if labels is not None else deepcopy(self.labels)
            names = names if names is not None else deepcopy(self.names)
        if levels is not None:
            new_index = new_index.set_levels(levels)
        if labels is not None:
            new_index = new_index.set_labels(labels)
        if names is not None:
            new_index = new_index.set_names(names)
        if dtype:
            new_index = new_index.astype(dtype)
        return new_index
