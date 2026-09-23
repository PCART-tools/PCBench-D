    def _get_grouper(self, obj):

        """
        Parameters
        ----------
        obj : the subject object

        Returns
        -------
        a tuple of binner, grouper, obj (possibly sorted)
        """

        self._set_grouper(obj)
        return self.binner, self.grouper, self.obj
