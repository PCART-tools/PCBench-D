    def clip(self, lower=None, upper=None, out=None, axis=None):
        """
        Trim values at input threshold(s)

        Parameters
        ----------
        lower : float or array_like, default None
        upper : float or array_like, default None
        axis : int or string axis name, optional
            Align object with lower and upper along the given axis.

        Returns
        -------
        clipped : Series

        Examples
        --------
        >>> df
          0         1
        0  0.335232 -1.256177
        1 -1.367855  0.746646
        2  0.027753 -1.176076
        3  0.230930 -0.679613
        4  1.261967  0.570967
        >>> df.clip(-1.0, 0.5)
                  0         1
        0  0.335232 -1.000000
        1 -1.000000  0.500000
        2  0.027753 -1.000000
        3  0.230930 -0.679613
        4  0.500000  0.500000
        >>> t
        0   -0.3
        1   -0.2
        2   -0.1
        3    0.0
        4    0.1
        dtype: float64
        >>> df.clip(t, t + 1, axis=0)
                  0         1
        0  0.335232 -0.300000
        1 -0.200000  0.746646
        2  0.027753 -0.100000
        3  0.230930  0.000000
        4  1.100000  0.570967
        """
        if out is not None:  # pragma: no cover
            raise Exception('out argument is not supported yet')

        # GH 2747 (arguments were reversed)
        if lower is not None and upper is not None:
            if lib.isscalar(lower) and lib.isscalar(upper):
                lower, upper = min(lower, upper), max(lower, upper)

        result = self
        if lower is not None:
            result = result.clip_lower(lower, axis)
        if upper is not None:
            result = result.clip_upper(upper, axis)

        return result
