    def sample(self, n=None, frac=None, replace=False, weights=None,
               random_state=None, axis=None):
        """
        Returns a random sample of items from an axis of object.

        .. versionadded:: 0.16.1

        Parameters
        ----------
        n : int, optional
            Number of items from axis to return. Cannot be used with `frac`.
            Default = 1 if `frac` = None.
        frac : float, optional
            Fraction of axis items to return. Cannot be used with `n`.
        replace : boolean, optional
            Sample with or without replacement. Default = False.
        weights : str or ndarray-like, optional
            Default 'None' results in equal probability weighting.
            If passed a Series, will align with target object on index. Index
            values in weights not found in sampled object will be ignored and
            index values in sampled object not in weights will be assigned
            weights of zero.
            If called on a DataFrame, will accept the name of a column
            when axis = 0.
            Unless weights are a Series, weights must be same length as axis
            being sampled.
            If weights do not sum to 1, they will be normalized to sum to 1.
            Missing values in the weights column will be treated as zero.
            inf and -inf values not allowed.
        random_state : int or numpy.random.RandomState, optional
            Seed for the random number generator (if int), or numpy RandomState
            object.
        axis : int or string, optional
            Axis to sample. Accepts axis number or name. Default is stat axis
            for given data type (0 for Series and DataFrames, 1 for Panels).

        Returns
        -------
        A new object of same type as caller.

        Examples
        --------

        Generate an example ``Series`` and ``DataFrame``:

        >>> s = pd.Series(np.random.randn(50))
        >>> s.head()
        0   -0.038497
        1    1.820773
        2   -0.972766
        3   -1.598270
        4   -1.095526
        dtype: float64
        >>> df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))
        >>> df.head()
                  A         B         C         D
        0  0.016443 -2.318952 -0.566372 -1.028078
        1 -1.051921  0.438836  0.658280 -0.175797
        2 -1.243569 -0.364626 -0.215065  0.057736
        3  1.768216  0.404512 -0.385604 -1.457834
        4  1.072446 -1.137172  0.314194 -0.046661

        Next extract a random sample from both of these objects...

        3 random elements from the ``Series``:

        >>> s.sample(n=3)
        27   -0.994689
        55   -1.049016
        67   -0.224565
        dtype: float64

        And a random 10% of the ``DataFrame`` with replacement:

        >>> df.sample(frac=0.1, replace=True)
                   A         B         C         D
        35  1.981780  0.142106  1.817165 -0.290805
        49 -1.336199 -0.448634 -0.789640  0.217116
        40  0.823173 -0.078816  1.009536  1.015108
        15  1.421154 -0.055301 -1.922594 -0.019696
        6  -0.148339  0.832938  1.787600 -1.383767
        """

        if axis is None:
            axis = self._stat_axis_number

        axis = self._get_axis_number(axis)
        axis_length = self.shape[axis]

        # Process random_state argument
        rs = com._random_state(random_state)

        # Check weights for compliance
        if weights is not None:

            # If a series, align with frame
            if isinstance(weights, pd.Series):
                weights = weights.reindex(self.axes[axis])

            # Strings acceptable if a dataframe and axis = 0
            if isinstance(weights, string_types):
                if isinstance(self, pd.DataFrame):
                    if axis == 0:
                        try:
                            weights = self[weights]
                        except KeyError:
                            raise KeyError("String passed to weights not a "
                                           "valid column")
                    else:
                        raise ValueError("Strings can only be passed to "
                                         "weights when sampling from rows on "
                                         "a DataFrame")
                else:
                    raise ValueError("Strings cannot be passed as weights "
                                     "when sampling from a Series or Panel.")

            weights = pd.Series(weights, dtype='float64')

            if len(weights) != axis_length:
                raise ValueError("Weights and axis to be sampled must be of "
                                 "same length")

            if (weights == np.inf).any() or (weights == -np.inf).any():
                raise ValueError("weight vector may not include `inf` values")

            if (weights < 0).any():
                raise ValueError("weight vector many not include negative "
                                 "values")

            # If has nan, set to zero.
            weights = weights.fillna(0)

            # Renormalize if don't sum to 1
            if weights.sum() != 1:
                if weights.sum() != 0:
                    weights = weights / weights.sum()
                else:
                    raise ValueError("Invalid weights: weights sum to zero")

            weights = weights.values

        # If no frac or n, default to n=1.
        if n is None and frac is None:
            n = 1
        elif n is not None and frac is None and n % 1 != 0:
            raise ValueError("Only integers accepted as `n` values")
        elif n is None and frac is not None:
            n = int(round(frac * axis_length))
        elif n is not None and frac is not None:
            raise ValueError('Please enter a value for `frac` OR `n`, not '
                             'both')

        # Check for negative sizes
        if n < 0:
            raise ValueError("A negative number of rows requested. Please "
                             "provide positive value.")

        locs = rs.choice(axis_length, size=n, replace=replace, p=weights)
        return self.take(locs, axis=axis, is_copy=False)
