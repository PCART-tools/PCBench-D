    def rename(self, name, inplace=False):
        """
        Set new names on index. Defaults to returning new index.

        Parameters
        ----------
        name : str or list
            name to set
        inplace : bool
            if True, mutates in place

        Returns
        -------
        new index (of same type and class...etc) [if inplace, returns None]
        """
        return self.set_names([name], inplace=inplace)
