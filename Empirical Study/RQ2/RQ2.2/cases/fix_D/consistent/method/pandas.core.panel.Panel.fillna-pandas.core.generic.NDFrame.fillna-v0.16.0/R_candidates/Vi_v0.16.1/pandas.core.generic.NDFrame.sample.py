    def sample(self, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None):
        """
        Returns a random sample of items from an axis of object.

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
            If called on a DataFrame, will accept the name of a column
            when axis = 0.
            Weights must be same length as axis being sampled.
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
        Same type as caller.
        """

        if axis is None:
            axis = self._stat_axis_number

        axis = self._get_axis_number(axis)
        axis_length = self.shape[axis]

        # Process random_state argument
        rs = com._random_state(random_state)

        # Check weights for compliance
        if weights is not None:

            # Strings acceptable if a dataframe and axis = 0
            if isinstance(weights, string_types):
                if isinstance(self, pd.DataFrame):
                    if axis == 0:
                        try:
                            weights = self[weights]
                        except KeyError:
                            raise KeyError("String passed to weights not a valid column")
                    else:
                        raise ValueError("Strings can only be passed to weights when sampling from rows on a DataFrame")
                else:
                    raise ValueError("Strings cannot be passed as weights when sampling from a Series or Panel.")

            weights = pd.Series(weights, dtype='float64')

            if len(weights) != axis_length:
                raise ValueError("Weights and axis to be sampled must be of same length")

            if (weights == np.inf).any() or (weights == -np.inf).any():
                raise ValueError("weight vector may not include `inf` values")

            if (weights < 0).any():
                raise ValueError("weight vector many not include negative values")

            # If has nan, set to zero.
            weights = weights.fillna(0)

            # Renormalize if don't sum to 1
            if weights.sum() != 1:
                weights = weights / weights.sum()

            weights = weights.values

        # If no frac or n, default to n=1.
        if n is None and frac is None:
            n = 1
        elif n is not None and frac is None and n % 1 != 0:
            raise ValueError("Only integers accepted as `n` values")
        elif n is None and frac is not None:
            n = int(round(frac * axis_length))
        elif n is not None and frac is not None:
            raise ValueError('Please enter a value for `frac` OR `n`, not both')

        # Check for negative sizes
        if n < 0:
            raise ValueError("A negative number of rows requested. Please provide positive value.")

        locs = rs.choice(axis_length, size=n, replace=replace, p=weights)
        return self.take(locs, axis=axis)
