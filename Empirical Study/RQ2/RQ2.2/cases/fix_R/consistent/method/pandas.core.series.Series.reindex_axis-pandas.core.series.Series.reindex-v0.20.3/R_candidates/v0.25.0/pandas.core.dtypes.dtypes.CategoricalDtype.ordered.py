    @property
    def ordered(self) -> OrderedType:
        """
        Whether the categories have an ordered relationship.
        """
        # TODO: remove if block when ordered=None as default is deprecated
        if self._ordered_from_sentinel and self._ordered is None:
            # warn when accessing ordered if ordered=None and None was not
            # explicitly passed to the constructor
            msg = (
                "Constructing a CategoricalDtype without specifying "
                "`ordered` will default to `ordered=False` in a future "
                "version; `ordered=None` must be explicitly passed."
            )
            warnings.warn(msg, FutureWarning, stacklevel=2)
        return self._ordered
