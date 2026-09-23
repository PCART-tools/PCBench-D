    @final
    def _set_grouper(self, obj: NDFrame, sort: bool = False) -> None:
        """
        given an object and the specifications, setup the internal grouper
        for this particular specification

        Parameters
        ----------
        obj : Series or DataFrame
        sort : bool, default False
            whether the resulting grouper should be sorted
        """
        assert obj is not None

        if self.key is not None and self.level is not None:
            raise ValueError("The Grouper cannot specify both a key and a level!")

        # Keep self.grouper value before overriding
        if self._grouper is None:
            # TODO: What are we assuming about subsequent calls?
            self._grouper = self._gpr_index
            self._indexer = self.indexer

        # the key must be a valid info item
        if self.key is not None:
            key = self.key
            # The 'on' is already defined
            if getattr(self._gpr_index, "name", None) == key and isinstance(
                obj, Series
            ):
                # Sometimes self._grouper will have been resorted while
                # obj has not. In this case there is a mismatch when we
                # call self._grouper.take(obj.index) so we need to undo the sorting
                # before we call _grouper.take.
                assert self._grouper is not None
                if self._indexer is not None:
                    reverse_indexer = self._indexer.argsort()
                    unsorted_ax = self._grouper.take(reverse_indexer)
                    ax = unsorted_ax.take(obj.index)
                else:
                    ax = self._grouper.take(obj.index)
            else:
                if key not in obj._info_axis:
                    raise KeyError(f"The grouper name {key} is not found")
                ax = Index(obj[key], name=key)

        else:
            ax = obj._get_axis(self.axis)
            if self.level is not None:
                level = self.level

                # if a level is given it must be a mi level or
                # equivalent to the axis name
                if isinstance(ax, MultiIndex):
                    level = ax._get_level_number(level)
                    ax = Index(ax._get_level_values(level), name=ax.names[level])

                else:
                    if level not in (0, ax.name):
                        raise ValueError(f"The level {level} is not valid")

        # possibly sort
        if (self.sort or sort) and not ax.is_monotonic_increasing:
            # use stable sort to support first, last, nth
            # TODO: why does putting na_position="first" fix datetimelike cases?
            indexer = self.indexer = ax.array.argsort(
                kind="mergesort", na_position="first"
            )
            ax = ax.take(indexer)
            obj = obj.take(indexer, axis=self.axis)

        # error: Incompatible types in assignment (expression has type
        # "NDFrameT", variable has type "None")
        self.obj = obj  # type: ignore[assignment]
        self._gpr_index = ax
