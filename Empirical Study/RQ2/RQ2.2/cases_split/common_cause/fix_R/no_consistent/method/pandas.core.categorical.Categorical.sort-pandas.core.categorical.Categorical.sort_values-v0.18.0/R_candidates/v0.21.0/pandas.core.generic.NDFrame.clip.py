    def clip(self, lower=None, upper=None, axis=None, inplace=False,
             *args, **kwargs):
        """
        Trim values at input threshold(s).

        Parameters
        ----------
        lower : float or array_like, default None
        upper : float or array_like, default None
        axis : int or string axis name, optional
            Align object with lower and upper along the given axis.
        inplace : boolean, default False
            Whether to perform the operation in place on the data
                .. versionadded:: 0.21.0

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
        if isinstance(self, ABCPanel):
            raise NotImplementedError("clip is not supported yet for panels")

        inplace = validate_bool_kwarg(inplace, 'inplace')

        axis = nv.validate_clip_with_axis(axis, args, kwargs)

        # GH 17276
        # numpy doesn't like NaN as a clip value
        # so ignore
        if np.any(pd.isnull(lower)):
            lower = None
        if np.any(pd.isnull(upper)):
            upper = None

        # GH 2747 (arguments were reversed)
        if lower is not None and upper is not None:
            if is_scalar(lower) and is_scalar(upper):
                lower, upper = min(lower, upper), max(lower, upper)

        # fast-path for scalars
        if ((lower is None or (is_scalar(lower) and is_number(lower))) and
                (upper is None or (is_scalar(upper) and is_number(upper)))):
            return self._clip_with_scalar(lower, upper, inplace=inplace)

        result = self
        if lower is not None:
            result = result.clip_lower(lower, axis, inplace=inplace)
        if upper is not None:
            if inplace:
                result = self
            result = result.clip_upper(upper, axis, inplace=inplace)

        return result
