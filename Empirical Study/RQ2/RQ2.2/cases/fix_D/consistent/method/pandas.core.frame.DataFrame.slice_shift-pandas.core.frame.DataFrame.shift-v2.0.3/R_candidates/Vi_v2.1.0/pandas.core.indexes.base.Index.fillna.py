    def fillna(self, value=None, downcast=lib.no_default):
        """
        Fill NA/NaN values with the specified value.

        Parameters
        ----------
        value : scalar
            Scalar value to use to fill holes (e.g. 0).
            This value cannot be a list-likes.
        downcast : dict, default is None
            A dict of item->dtype of what to downcast if possible,
            or the string 'infer' which will try to downcast to an appropriate
            equal type (e.g. float64 to int64 if possible).

            .. deprecated:: 2.1.0

        Returns
        -------
        Index

        See Also
        --------
        DataFrame.fillna : Fill NaN values of a DataFrame.
        Series.fillna : Fill NaN Values of a Series.

        Examples
        --------
        >>> idx = pd.Index([np.nan, np.nan, 3])
        >>> idx.fillna(0)
        Index([0.0, 0.0, 3.0], dtype='float64')
        """
        if not is_scalar(value):
            raise TypeError(f"'value' must be a scalar, passed: {type(value).__name__}")
        if downcast is not lib.no_default:
            warnings.warn(
                f"The 'downcast' keyword in {type(self).__name__}.fillna is "
                "deprecated and will be removed in a future version. "
                "It was previously silently ignored.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        else:
            downcast = None

        if self.hasnans:
            result = self.putmask(self._isnan, value)
            if downcast is None:
                # no need to care metadata other than name
                # because it can't have freq if it has NaTs
                # _with_infer needed for test_fillna_categorical
                return Index._with_infer(result, name=self.name)
            raise NotImplementedError(
                f"{type(self).__name__}.fillna does not support 'downcast' "
                "argument values other than 'None'."
            )
        return self._view()
