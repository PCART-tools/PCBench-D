    def is_bounded_0_1(self, params=None):
        """
        Returns a boolean indicating if the function is bounded in the [0,1]
        interval for a particular set of additional parameters.

        Parameters
        ----------

        params : list
            The list of additional parameters. Default None.

        Returns
        -------

        out : bool
            True if the function is bounded in the [0,1] interval for
            parameters 'params'. Otherwise False.

        """

        return self._bounded_0_1(params)
