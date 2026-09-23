    @final
    def sample(
        self,
        n: int | None = None,
        frac: float | None = None,
        replace: bool = False,
        weights: Sequence | Series | None = None,
        random_state: RandomState | None = None,
    ):
        """
        Return a random sample of items from each group.

        You can use `random_state` for reproducibility.

        Parameters
        ----------
        n : int, optional
            Number of items to return for each group. Cannot be used with
            `frac` and must be no larger than the smallest group unless
            `replace` is True. Default is one if `frac` is None.
        frac : float, optional
            Fraction of items to return. Cannot be used with `n`.
        replace : bool, default False
            Allow or disallow sampling of the same row more than once.
        weights : list-like, optional
            Default None results in equal probability weighting.
            If passed a list-like then values must have the same length as
            the underlying DataFrame or Series object and will be used as
            sampling probabilities after normalization within each group.
            Values must be non-negative with at least one positive element
            within each group.
        random_state : int, array-like, BitGenerator, np.random.RandomState, np.random.Generator, optional
            If int, array-like, or BitGenerator, seed for random number generator.
            If np.random.RandomState or np.random.Generator, use as given.

            .. versionchanged:: 1.4.0

                np.random.Generator objects now accepted

        Returns
        -------
        Series or DataFrame
            A new object of same type as caller containing items randomly
            sampled within each group from the caller object.

        See Also
        --------
        DataFrame.sample: Generate random samples from a DataFrame object.
        numpy.random.choice: Generate a random sample from a given 1-D numpy
            array.

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {"a": ["red"] * 2 + ["blue"] * 2 + ["black"] * 2, "b": range(6)}
        ... )
        >>> df
               a  b
        0    red  0
        1    red  1
        2   blue  2
        3   blue  3
        4  black  4
        5  black  5

        Select one row at random for each distinct value in column a. The
        `random_state` argument can be used to guarantee reproducibility:

        >>> df.groupby("a").sample(n=1, random_state=1)
               a  b
        4  black  4
        2   blue  2
        1    red  1

        Set `frac` to sample fixed proportions rather than counts:

        >>> df.groupby("a")["b"].sample(frac=0.5, random_state=2)
        5    5
        2    2
        0    0
        Name: b, dtype: int64

        Control sample probabilities within groups by setting weights:

        >>> df.groupby("a").sample(
        ...     n=1,
        ...     weights=[1, 1, 1, 0, 0, 1],
        ...     random_state=1,
        ... )
               a  b
        5  black  5
        2   blue  2
        0    red  0
        """  # noqa: E501
        if self._selected_obj.empty:
            # GH48459 prevent ValueError when object is empty
            return self._selected_obj
        size = sample.process_sampling_size(n, frac, replace)
        if weights is not None:
            weights_arr = sample.preprocess_weights(
                self._selected_obj, weights, axis=self.axis
            )

        random_state = com.random_state(random_state)

        group_iterator = self.grouper.get_iterator(self._selected_obj, self.axis)

        sampled_indices = []
        for labels, obj in group_iterator:
            grp_indices = self.indices[labels]
            group_size = len(grp_indices)
            if size is not None:
                sample_size = size
            else:
                assert frac is not None
                sample_size = round(frac * group_size)

            grp_sample = sample.sample(
                group_size,
                size=sample_size,
                replace=replace,
                weights=None if weights is None else weights_arr[grp_indices],
                random_state=random_state,
            )
            sampled_indices.append(grp_indices[grp_sample])

        sampled_indices = np.concatenate(sampled_indices)
        return self._selected_obj.take(sampled_indices, axis=self.axis)
