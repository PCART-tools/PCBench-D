    def get_loc(self, key, method=None, tolerance=None):
        """
        Get integer location, slice or boolean mask for requested label.

        Parameters
        ----------
        key : label
        method : {None, 'pad'/'ffill', 'backfill'/'bfill', 'nearest'}, optional
            * default: exact matches only.
            * pad / ffill: find the PREVIOUS index value if no exact match.
            * backfill / bfill: use NEXT index value if no exact match
            * nearest: use the NEAREST index value if no exact match. Tied
              distances are broken by preferring the larger index value.
        tolerance : int or float, optional
            Maximum distance from index value for inexact matches. The value of
            the index at the matching location must satisfy the equation
            ``abs(index[loc] - key) <= tolerance``.

        Returns
        -------
        loc : int if unique index, slice if monotonic index, else mask

        Examples
        --------
        >>> unique_index = pd.Index(list('abc'))
        >>> unique_index.get_loc('b')
        1

        >>> monotonic_index = pd.Index(list('abbc'))
        >>> monotonic_index.get_loc('b')
        slice(1, 3, None)

        >>> non_monotonic_index = pd.Index(list('abcb'))
        >>> non_monotonic_index.get_loc('b')
        array([False,  True, False,  True])
        """
        if method is None:
            if tolerance is not None:
                raise ValueError(
                    "tolerance argument only valid if using pad, "
                    "backfill or nearest lookups"
                )
            casted_key = self._maybe_cast_indexer(key)
            try:
                return self._engine.get_loc(casted_key)
            except KeyError as err:
                raise KeyError(key) from err
            except TypeError:
                # If we have a listlike key, _check_indexing_error will raise
                #  InvalidIndexError. Otherwise we fall through and re-raise
                #  the TypeError.
                self._check_indexing_error(key)
                raise

        # GH#42269
        warnings.warn(
            f"Passing method to {type(self).__name__}.get_loc is deprecated "
            "and will raise in a future version. Use "
            "index.get_indexer([item], method=...) instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )

        if is_scalar(key) and isna(key) and not self.hasnans:
            raise KeyError(key)

        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance, np.asarray(key))

        indexer = self.get_indexer([key], method=method, tolerance=tolerance)
        if indexer.ndim > 1 or indexer.size > 1:
            raise TypeError("get_loc requires scalar valued input")
        loc = indexer.item()
        if loc == -1:
            raise KeyError(key)
        return loc
