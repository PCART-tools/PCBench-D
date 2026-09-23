    @final
    @_maybe_return_indexers
    def join(
        self,
        other: Index,
        *,
        how: JoinHow = "left",
        level: Level = None,
        return_indexers: bool = False,
        sort: bool = False,
    ) -> Index | tuple[Index, npt.NDArray[np.intp] | None, npt.NDArray[np.intp] | None]:
        """
        Compute join_index and indexers to conform data structures to the new index.

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

        if len(other) == 0:
            if how in ("left", "outer"):
                join_index = self._view()
                rindexer = np.broadcast_to(np.intp(-1), len(join_index))
                return join_index, None, rindexer
            elif how in ("right", "inner", "cross"):
                join_index = other._view()
                lindexer = np.array([])
                return join_index, lindexer, None

        if len(self) == 0:
            if how in ("right", "outer"):
                join_index = other._view()
                lindexer = np.broadcast_to(np.intp(-1), len(join_index))
                return join_index, lindexer, None
            elif how in ("left", "inner", "cross"):
                join_index = self._view()
                rindexer = np.array([])
                return join_index, None, rindexer

        if self._join_precedence < other._join_precedence:
            flip: dict[JoinHow, JoinHow] = {"right": "left", "left": "right"}
            how = flip.get(how, how)
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
            if self.is_monotonic_increasing and other.is_monotonic_increasing:
                if not is_interval_dtype(self.dtype):
                    # otherwise we will fall through to _join_via_get_indexer
                    # GH#39133
                    # go through object dtype for ea till engine is supported properly
                    return self._join_monotonic(other, how=how)
            else:
                return self._join_non_unique(other, how=how)
        elif (
            # GH48504: exclude MultiIndex to avoid going through MultiIndex._values
            self.is_monotonic_increasing
            and other.is_monotonic_increasing
            and self._can_use_libjoin
            and not isinstance(self, ABCMultiIndex)
            and not is_categorical_dtype(self.dtype)
        ):
            # Categorical is monotonic if data are ordered as categories, but join can
            #  not handle this in case of not lexicographically monotonic GH#38502
            try:
                return self._join_monotonic(other, how=how)
            except TypeError:
                # object dtype; non-comparable objects
                pass

        return self._join_via_get_indexer(other, how, sort)
