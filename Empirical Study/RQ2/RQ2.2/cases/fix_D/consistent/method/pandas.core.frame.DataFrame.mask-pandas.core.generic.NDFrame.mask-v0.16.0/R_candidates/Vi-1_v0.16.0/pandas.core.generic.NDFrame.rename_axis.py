    def rename_axis(self, mapper, axis=0, copy=True, inplace=False):
        """
        Alter index and / or columns using input function or functions.
        Function / dict values must be unique (1-to-1). Labels not contained in
        a dict / Series will be left as-is.

        Parameters
        ----------
        mapper : dict-like or function, optional
        axis : int or string, default 0
        copy : boolean, default True
            Also copy underlying data
        inplace : boolean, default False

        Returns
        -------
        renamed : type of caller
        """
        axis = self._get_axis_name(axis)
        d = {'copy': copy, 'inplace': inplace}
        d[axis] = mapper
        return self.rename(**d)
