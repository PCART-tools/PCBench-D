    @final
    def to_native_types(self, slicer=None, **kwargs) -> np.ndarray:
        """
        Format specified values of `self` and return them.

        .. deprecated:: 1.2.0

        Parameters
        ----------
        slicer : int, array-like
            An indexer into `self` that specifies which values
            are used in the formatting process.
        kwargs : dict
            Options for specifying how the values should be formatted.
            These options include the following:

            1) na_rep : str
                The value that serves as a placeholder for NULL values
            2) quoting : bool or None
                Whether or not there are quoted values in `self`
            3) date_format : str
                The format used to represent date-like values.

        Returns
        -------
        numpy.ndarray
            Formatted values.
        """
        warnings.warn(
            "The 'to_native_types' method is deprecated and will be removed in "
            "a future version. Use 'astype(str)' instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        values = self
        if slicer is not None:
            values = values[slicer]
        return values._format_native_types(**kwargs)
