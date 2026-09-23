    def get_group(self, name, obj=None):
        """
        Constructs NDFrame from group with provided name

        Parameters
        ----------
        name : object
            the name of the group to get as a DataFrame
        obj : NDFrame, default None
            the NDFrame to take the DataFrame out of.  If
            it is None, the object groupby was called on will
            be used

        Returns
        -------
        group : type of obj
        """
        if obj is None:
            obj = self._selected_obj

        inds = self._get_index(name)
        if not len(inds):
            raise KeyError(name)

        return obj._take(inds, axis=self.axis, convert=False)
