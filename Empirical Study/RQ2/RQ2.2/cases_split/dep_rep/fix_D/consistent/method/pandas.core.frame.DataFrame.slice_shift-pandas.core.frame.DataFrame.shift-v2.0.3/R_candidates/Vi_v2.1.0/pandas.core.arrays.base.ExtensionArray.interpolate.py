    def interpolate(
        self,
        *,
        method: InterpolateOptions,
        axis: int,
        index: Index,
        limit,
        limit_direction,
        limit_area,
        fill_value,
        copy: bool,
        **kwargs,
    ) -> Self:
        """
        See DataFrame.interpolate.__doc__.

        Examples
        --------
        >>> arr = pd.arrays.NumpyExtensionArray(np.array([0, 1, np.nan, 3]))
        >>> arr.interpolate(method="linear",
        ...                 limit=3,
        ...                 limit_direction="forward",
        ...                 index=pd.Index([1, 2, 3, 4]),
        ...                 fill_value=1,
        ...                 copy=False,
        ...                 axis=0,
        ...                 limit_area="inside"
        ...                 )
        <NumpyExtensionArray>
        [0.0, 1.0, 2.0, 3.0]
        Length: 4, dtype: float64
        """
        # NB: we return type(self) even if copy=False
        raise NotImplementedError(
            f"{type(self).__name__} does not implement interpolate"
        )
