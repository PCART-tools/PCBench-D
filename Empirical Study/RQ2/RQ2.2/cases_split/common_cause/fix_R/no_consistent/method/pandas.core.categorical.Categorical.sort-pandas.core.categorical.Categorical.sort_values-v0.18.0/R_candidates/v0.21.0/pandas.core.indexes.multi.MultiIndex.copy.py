    def copy(self, names=None, dtype=None, levels=None, labels=None,
             deep=False, _set_identity=False, **kwargs):
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
        name = kwargs.get('name')
        names = self._validate_names(name=name, names=names, deep=deep)

        if deep:
            from copy import deepcopy
            if levels is None:
                levels = deepcopy(self.levels)
            if labels is None:
                labels = deepcopy(self.labels)
        else:
            if levels is None:
                levels = self.levels
            if labels is None:
                labels = self.labels
        return MultiIndex(levels=levels, labels=labels, names=names,
                          sortorder=self.sortorder, verify_integrity=False,
                          _set_identity=_set_identity)
