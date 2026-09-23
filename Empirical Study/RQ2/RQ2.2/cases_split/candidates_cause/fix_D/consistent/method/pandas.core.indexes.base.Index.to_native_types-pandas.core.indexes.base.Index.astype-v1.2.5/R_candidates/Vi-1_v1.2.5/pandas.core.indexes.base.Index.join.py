    def join(self, other, how="left", level=None, return_indexers=False, sort=False):
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

        # try to figure out the join level
        # GH3662
        if level is None and (self_is_mi or other_is_mi):

            # have the same levels/names so a simple join
            if self.names == other.names:
                pass
            else:
                return self._join_multi(other, how=how, return_indexers=return_indexers)

        # join on the level
        if level is not None and (self_is_mi or other_is_mi):
            return self._join_level(
                other, level, how=how, return_indexers=return_indexers
            )

        if len(other) == 0 and how in ("left", "outer"):
            join_index = self._shallow_copy()
            if return_indexers:
                rindexer = np.repeat(-1, len(join_index))
                return join_index, None, rindexer
            else:
                return join_index

        if len(self) == 0 and how in ("right", "outer"):
            join_index = other._shallow_copy()
            if return_indexers:
                lindexer = np.repeat(-1, len(join_index))
                return join_index, lindexer, None
            else:
                return join_index

        if self._join_precedence < other._join_precedence:
            how = {"right": "left", "left": "right"}.get(how, how)
            result = other.join(
                self, how=how, level=level, return_indexers=return_indexers
            )
            if return_indexers:
                x, y, z = result
                result = x, z, y
            return result

        if not is_dtype_equal(self.dtype, other.dtype):
            this = self.astype("O")
            other = other.astype("O")
            return this.join(other, how=how, return_indexers=return_indexers)

        _validate_join_method(how)

        if not self.is_unique and not other.is_unique:
            return self._join_non_unique(
                other, how=how, return_indexers=return_indexers
            )
        elif not self.is_unique or not other.is_unique:
            if self.is_monotonic and other.is_monotonic:
                return self._join_monotonic(
                    other, how=how, return_indexers=return_indexers
                )
            else:
                return self._join_non_unique(
                    other, how=how, return_indexers=return_indexers
                )
        elif self.is_monotonic and other.is_monotonic:
            try:
                return self._join_monotonic(
                    other, how=how, return_indexers=return_indexers
                )
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

        if return_indexers:
            if join_index is self:
                lindexer = None
            else:
                lindexer = self.get_indexer(join_index)
            if join_index is other:
                rindexer = None
            else:
                rindexer = other.get_indexer(join_index)
            return join_index, lindexer, rindexer
        else:
            return join_index
