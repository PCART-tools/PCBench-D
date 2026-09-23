    def clip_upper(self, threshold, axis=None, inplace=False):
        """
        Trim values above a given threshold.

        .. deprecated:: 0.24.0
            Use clip(upper=threshold) instead.

        Elements above the `threshold` will be changed to match the
        `threshold` value(s). Threshold can be a single value or an array,
        in the latter case it performs the truncation element-wise.

        Parameters
        ----------
        threshold : numeric or array-like
            Maximum value allowed. All values above threshold will be set to
            this value.

            * float : every value is compared to `threshold`.
            * array-like : The shape of `threshold` should match the object
              it's compared to. When `self` is a Series, `threshold` should be
              the length. When `self` is a DataFrame, `threshold` should 2-D
              and the same shape as `self` for ``axis=None``, or 1-D and the
              same length as the axis being compared.

        axis : {0 or 'index', 1 or 'columns'}, default 0
            Align object with `threshold` along the given axis.
        inplace : bool, default False
            Whether to perform the operation in place on the data.

            .. versionadded:: 0.21.0

        Returns
        -------
        Series or DataFrame
            Original data with values trimmed.

        See Also
        --------
        Series.clip : General purpose method to trim Series values to given
            threshold(s).
        DataFrame.clip : General purpose method to trim DataFrame values to
            given threshold(s).

        Examples
        --------
        >>> s = pd.Series([1, 2, 3, 4, 5])
        >>> s
        0    1
        1    2
        2    3
        3    4
        4    5
        dtype: int64

        >>> s.clip(upper=3)
        0    1
        1    2
        2    3
        3    3
        4    3
        dtype: int64

        >>> elemwise_thresholds = [5, 4, 3, 2, 1]
        >>> elemwise_thresholds
        [5, 4, 3, 2, 1]

        >>> s.clip(upper=elemwise_thresholds)
        0    1
        1    2
        2    3
        3    2
        4    1
        dtype: int64
        """
        warnings.warn(
            "clip_upper(threshold) is deprecated, " "use clip(upper=threshold) instead",
            FutureWarning,
            stacklevel=2,
        )
        return self._clip_with_one_bound(
            threshold, method=self.le, axis=axis, inplace=inplace
        )
