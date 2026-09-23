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
        self_is_mi = isinstance(self, ABCMultiIndex)
        other_is_mi = isinstance(other, ABCMultiIndex)

        lindexer: np.ndarray | None
        rindexer: np.ndarray | None

        # try to figure out the join level
        # GH3662
        if level is None and (self_is_mi or other_is_mi):

            # have the same levels/names so a simple join
            if self.names == other.names:
                pass
            else:
                return self._join_multi(other, how=how)

        # join on the level
        if level is not None and (self_is_mi or other_is_mi):
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
            this = self.astype("O")
            other = other.astype("O")
            return this.join(other, how=how, return_indexers=True)

        _validate_join_method(how)

        if not self.is_unique and not other.is_unique:
            return self._join_non_unique(other, how=how)
        elif not self.is_unique or not other.is_unique:
            if self.is_monotonic and other.is_monotonic:
                return self._join_monotonic(other, how=how)
            else:
                return self._join_non_unique(other, how=how)
        elif (
            self.is_monotonic
            and other.is_monotonic
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
                pass

        if how == "left":
            join_index = self
        elif how == "right":
            join_index = other
        elif how == "inner":
            # TODO: sort=False here for backwards compat. It may
            # be better to use the sort parameter passed into join
            join_index = self.intersection(other, sort=False)
        elif how == "outer":
            # TODO: sort=True here for backwards compat. It may
            # be better to use the sort parameter passed into join
            join_index = self.union(other)

        if sort:
            join_index = join_index.sort_values()

        if join_index is self:
            lindexer = None
        else:
            lindexer = self.get_indexer(join_index)
        if join_index is other:
            rindexer = None
        else:
            rindexer = other.get_indexer(join_index)
        return join_index, lindexer, rindexer
