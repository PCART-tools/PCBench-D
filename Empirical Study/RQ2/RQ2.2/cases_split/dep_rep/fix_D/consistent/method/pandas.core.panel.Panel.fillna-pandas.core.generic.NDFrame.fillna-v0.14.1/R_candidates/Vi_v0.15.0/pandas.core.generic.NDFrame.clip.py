    def clip(self, lower=None, upper=None, out=None):
        """
        Trim values at input threshold(s)

        Parameters
        ----------
        lower : float, default None
        upper : float, default None

        Returns
        -------
        clipped : Series
        """
        if out is not None:  # pragma: no cover
            raise Exception('out argument is not supported yet')

        # GH 2747 (arguments were reversed)
        if lower is not None and upper is not None:
            lower, upper = min(lower, upper), max(lower, upper)

        result = self
        if lower is not None:
            result = result.clip_lower(lower)
        if upper is not None:
            result = result.clip_upper(upper)

        return result
