    def clip_lower(self, threshold, axis=None, inplace=False):
        """
        Return copy of the input with values below a threshold truncated.

        Parameters
        ----------
        threshold : numeric or array-like
            Minimum value allowed. All values below threshold will be set to
            this value.

            * float : every value is compared to `threshold`.
            * array-like : The shape of `threshold` should match the object
              it's compared to. When `self` is a Series, `threshold` should be
              the length. When `self` is a DataFrame, `threshold` should 2-D
              and the same shape as `self` for ``axis=None``, or 1-D and the
              same length as the axis being compared.

        axis : {0 or 'index', 1 or 'columns'}, default 0
            Align `self` with `threshold` along the given axis.

        inplace : boolean, default False
            Whether to perform the operation in place on the data.

            .. versionadded:: 0.21.0

        See Also
        --------
        Series.clip : Return copy of input with values below and above
            thresholds truncated.
        Series.clip_upper : Return copy of input with values above
            threshold truncated.

        Returns
        -------
        clipped : same type as input

        Examples
        --------
        Series single threshold clipping:

        >>> s = pd.Series([5, 6, 7, 8, 9])
        >>> s.clip_lower(8)
        0    8
        1    8
        2    8
        3    8
        4    9
        dtype: int64

        Series clipping element-wise using an array of thresholds. `threshold`
        should be the same length as the Series.

        >>> elemwise_thresholds = [4, 8, 7, 2, 5]
        >>> s.clip_lower(elemwise_thresholds)
        0    5
        1    8
        2    7
        3    8
        4    9
        dtype: int64

        DataFrames can be compared to a scalar.

        >>> df = pd.DataFrame({"A": [1, 3, 5], "B": [2, 4, 6]})
        >>> df
           A  B
        0  1  2
        1  3  4
        2  5  6

        >>> df.clip_lower(3)
           A  B
        0  3  3
        1  3  4
        2  5  6

        Or to an array of values. By default, `threshold` should be the same
        shape as the DataFrame.

        >>> df.clip_lower(np.array([[3, 4], [2, 2], [6, 2]]))
           A  B
        0  3  4
        1  3  4
        2  6  6

        Control how `threshold` is broadcast with `axis`. In this case
        `threshold` should be the same length as the axis specified by
        `axis`.

        >>> df.clip_lower(np.array([3, 3, 5]), axis='index')
           A  B
        0  3  3
        1  3  4
        2  5  6

        >>> df.clip_lower(np.array([4, 5]), axis='columns')
           A  B
        0  4  5
        1  4  5
        2  5  6
        """
        return self._clip_with_one_bound(threshold, method=self.ge,
                                         axis=axis, inplace=inplace)
