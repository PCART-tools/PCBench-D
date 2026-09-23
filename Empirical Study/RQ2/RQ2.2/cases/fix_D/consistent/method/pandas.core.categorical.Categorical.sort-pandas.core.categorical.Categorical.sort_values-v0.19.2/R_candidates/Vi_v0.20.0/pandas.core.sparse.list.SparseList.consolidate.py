    def consolidate(self, inplace=True):
        """
        Internally consolidate chunks of data

        Parameters
        ----------
        inplace : boolean, default True
            Modify the calling object instead of constructing a new one

        Returns
        -------
        splist : SparseList
            If inplace=False, new object, otherwise reference to existing
            object
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        if not inplace:
            result = self.copy()
        else:
            result = self

        if result.is_consolidated:
            return result

        result._consolidate_inplace()
        return result
