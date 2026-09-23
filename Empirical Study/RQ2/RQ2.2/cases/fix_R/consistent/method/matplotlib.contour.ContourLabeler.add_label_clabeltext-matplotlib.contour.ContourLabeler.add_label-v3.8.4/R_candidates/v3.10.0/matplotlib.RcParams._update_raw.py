    def _update_raw(self, other_params):
        """
        Directly update the data from *other_params*, bypassing deprecation,
        backend and validation logic on both sides.

        This ``rcParams._update_raw(params)`` replaces the previous pattern
        ``dict.update(rcParams, params)``.

        Parameters
        ----------
        other_params : dict or `.RcParams`
            The input mapping from which to update.
        """
        if isinstance(other_params, RcParams):
            other_params = dict.items(other_params)
        dict.update(self, other_params)
