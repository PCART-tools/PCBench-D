    def union_many(self, others):
        """
        A bit of a hack to accelerate unioning a collection of indexes.
        """
        warnings.warn(
            "DatetimeIndex.union_many is deprecated and will be removed in "
            "a future version. Use obj.union instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )

        this = self

        for other in others:
            if not isinstance(this, DatetimeIndex):
                this = Index.union(this, other)
                continue

            if not isinstance(other, DatetimeIndex):
                try:
                    other = DatetimeIndex(other)
                except TypeError:
                    pass

            this, other = this._maybe_utc_convert(other)

            if len(self) and len(other) and this._can_fast_union(other):
                # union already has fastpath handling for empty cases
                this = this._fast_union(other)
            else:
                this = Index.union(this, other)

        res_name = get_unanimous_names(self, *others)[0]
        if this.name != res_name:
            return this.rename(res_name)
        return this
