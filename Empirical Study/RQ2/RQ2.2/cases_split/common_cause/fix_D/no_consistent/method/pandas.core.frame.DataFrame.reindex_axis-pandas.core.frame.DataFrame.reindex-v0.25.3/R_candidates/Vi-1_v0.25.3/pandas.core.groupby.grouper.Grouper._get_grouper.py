    def _get_grouper(self, obj, validate=True):
        """
        Parameters
        ----------
        obj : the subject object
        validate : boolean, default True
            if True, validate the grouper

        Returns
        -------
        a tuple of binner, grouper, obj (possibly sorted)
        """

        self._set_grouper(obj)
        self.grouper, exclusions, self.obj = _get_grouper(
            self.obj,
            [self.key],
            axis=self.axis,
            level=self.level,
            sort=self.sort,
            validate=validate,
        )
        return self.binner, self.grouper, self.obj
