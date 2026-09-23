    def clip(self, lower=None, upper=None, axis=None, inplace=False, *args, **kwargs):
        """
        Trim values at input threshold(s).

        Assigns values outside boundary to boundary values. Thresholds
        can be singular values or array like, and in the latter case
        the clipping is performed element-wise in the specified axis.

        Parameters
        ----------
        lower : float or array_like, default None
            Minimum threshold value. All values below this
            threshold will be set to it.
        upper : float or array_like, default None
            Maximum threshold value. All values above this
            threshold will be set to it.
        axis : int or str axis name, optional
            Align object with lower and upper along the given axis.
        inplace : bool, default False
            Whether to perform the operation in place on the data.

            .. versionadded:: 0.21.0
        *args, **kwargs
            Additional keywords have no effect but might be accepted
            for compatibility with numpy.

        Returns
        -------
        Series or DataFrame
            Same type as calling object with the values outside the
            clip boundaries replaced.

        Examples
        --------
        >>> data = {'col_0': [9, -3, 0, -1, 5], 'col_1': [-2, -7, 6, 8, -5]}
        >>> df = pd.DataFrame(data)
        >>> df
           col_0  col_1
        0      9     -2
        1     -3     -7
        2      0      6
        3     -1      8
        4      5     -5

        Clips per column using lower and upper thresholds:

        >>> df.clip(-4, 6)
           col_0  col_1
        0      6     -2
        1     -3     -4
        2      0      6
        3     -1      6
        4      5     -4

        Clips using specific lower and upper thresholds per column element:

        >>> t = pd.Series([2, -4, -1, 6, 3])
        >>> t
        0    2
        1   -4
        2   -1
        3    6
        4    3
        dtype: int64

        >>> df.clip(t, t + 4, axis=0)
           col_0  col_1
        0      6      2
        1     -3     -4
        2      0      3
        3      6      8
        4      5      3
        """
        inplace = validate_bool_kwarg(inplace, "inplace")

        axis = nv.validate_clip_with_axis(axis, args, kwargs)
        if axis is not None:
            axis = self._get_axis_number(axis)

        # GH 17276
        # numpy doesn't like NaN as a clip value
        # so ignore
        # GH 19992
        # numpy doesn't drop a list-like bound containing NaN
        if not is_list_like(lower) and np.any(pd.isnull(lower)):
            lower = None
        if not is_list_like(upper) and np.any(pd.isnull(upper)):
            upper = None

        # GH 2747 (arguments were reversed)
        if lower is not None and upper is not None:
            if is_scalar(lower) and is_scalar(upper):
                lower, upper = min(lower, upper), max(lower, upper)

        # fast-path for scalars
        if (lower is None or (is_scalar(lower) and is_number(lower))) and (
            upper is None or (is_scalar(upper) and is_number(upper))
        ):
            return self._clip_with_scalar(lower, upper, inplace=inplace)

        result = self
        if lower is not None:
            result = result._clip_with_one_bound(
                lower, method=self.ge, axis=axis, inplace=inplace
            )
        if upper is not None:
            if inplace:
                result = self
            result = result._clip_with_one_bound(
                upper, method=self.le, axis=axis, inplace=inplace
            )

        return result
