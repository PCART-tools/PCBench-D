    def check_params(self, params=None):
        """
        Returns a boolean indicating if the set of additional parameters is
        valid.

        Parameters
        ----------

        params : list
            The list of additional parameters. Default None.

        Returns
        -------

        out : bool
            True if 'params' is a valid set of additional parameters for the
            function. Otherwise False.

        """

        return self._check_params(params)
