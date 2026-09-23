    def _validate_read_indexer(self, key, indexer, axis):
        """
        Check that indexer can be used to return a result (e.g. at least one
        element was found, unless the list of keys was actually empty).

        Parameters
        ----------
        key : list-like
            Target labels (only used to show correct error message)
        indexer: array-like of booleans
            Indices corresponding to the key (with -1 indicating not found)
        axis: int
            Dimension on which the indexing is being made

        Raises
        ------
        KeyError
            If at least one key was requested none was found.
        """

        ax = self.obj._get_axis(axis)

        if len(key) == 0:
            return

        # Count missing values:
        missing = (indexer < 0).sum()

        if missing:
            if missing == len(indexer):
                raise KeyError(
                    u"None of [{key}] are in the [{axis}]".format(
                        key=key, axis=self.obj._get_axis_name(axis)))

            # we skip the warning on Categorical/Interval
            # as this check is actually done (check for
            # non-missing values), but a bit later in the
            # code, so we want to avoid warning & then
            # just raising

            _missing_key_warning = textwrap.dedent("""
            Passing list-likes to .loc or [] with any missing label will raise
            KeyError in the future, you can use .reindex() as an alternative.

            See the documentation here:
            https://pandas.pydata.org/pandas-docs/stable/indexing.html#deprecate-loc-reindex-listlike""")  # noqa

            if not (ax.is_categorical() or ax.is_interval()):
                warnings.warn(_missing_key_warning,
                              FutureWarning, stacklevel=5)
