    @final
    @_maybe_return_indexers
    def join(
        self,
        other,
        how: str_t = "left",
        level=None,
        return_indexers: bool = False,
        sort: bool = False,
    ):
        """
        Compute join_index and indexers to conform data
        structures to the new index.

        Parameters
        ----------
        other : Index
        how : {'left', 'right', 'inner', 'outer'}
        level : int or level name, default None
        return_indexers : bool, default False
        sort : bool, default False
            Sort the join keys lexicographically in the result Index. If False,
            the order of the join keys depends on the join type (how keyword).

        Returns
        -------
        join_index, (left_indexer, right_indexer)
        """
        other = ensure_index(other)

        if isinstance(self, ABCDatetimeIndex) and isinstance(other, ABCDatetimeIndex):
            if (self.tz is None) ^ (other.tz is None):
                # Raise instead of casting to object below.
                raise TypeError("Cannot join tz-naive with tz-aware DatetimeIndex")

        if not self._is_multi and not other._is_multi:
            # We have specific handling for MultiIndex below
            pself, pother = self._maybe_promote(other)
            if pself is not self or pother is not other:
                return pself.join(
                    pother, how=how, level=level, return_indexers=True, sort=sort
                )

        lindexer: np.ndarray | None
        rindexer: np.ndarray | None

        # try to figure out the join level
        # GH3662
        if level is None and (self._is_multi or other._is_multi):

            # have the same levels/names so a simple join
            if self.names == other.names:
                pass
            else:
                return self._join_multi(other, how=how)

        # join on the level
        if level is not None and (self._is_multi or other._is_multi):
            return self._join_level(other, level, how=how)

        if len(other) == 0 and how in ("left", "outer"):
            join_index = self._view()
            rindexer = np.repeat(np.intp(-1), len(join_index))
            return join_index, None, rindexer

        if len(self) == 0 and how in ("right", "outer"):
            join_index = other._view()
            lindexer = np.repeat(np.intp(-1), len(join_index))
            return join_index, lindexer, None

        if self._join_precedence < other._join_precedence:
            how = {"right": "left", "left": "right"}.get(how, how)
            join_index, lidx, ridx = other.join(
                self, how=how, level=level, return_indexers=True
            )
            lidx, ridx = ridx, lidx
            return join_index, lidx, ridx

        if not is_dtype_equal(self.dtype, other.dtype):
            dtype = self._find_common_type_compat(other)
            this = self.astype(dtype, copy=False)
            other = other.astype(dtype, copy=False)
            return this.join(other, how=how, return_indexers=True)

        _validate_join_method(how)

        if not self.is_unique and not other.is_unique:
            return self._join_non_unique(other, how=how)
        elif not self.is_unique or not other.is_unique:
            if self.is_monotonic and other.is_monotonic:
                if self._can_use_libjoin:
                    # otherwise we will fall through to _join_via_get_indexer
                    return self._join_monotonic(other, how=how)
            else:
                return self._join_non_unique(other, how=how)
        elif (
            self.is_monotonic
            and other.is_monotonic
            and self._can_use_libjoin
            and (
                not isinstance(self, ABCMultiIndex)
                or not any(is_categorical_dtype(dtype) for dtype in self.dtypes)
            )
        ):
            # Categorical is monotonic if data are ordered as categories, but join can
            #  not handle this in case of not lexicographically monotonic GH#38502
            try:
                return self._join_monotonic(other, how=how)
            except TypeError:
                # object dtype; non-comparable objects
                pass

        return self._join_via_get_indexer(other, how, sort)
