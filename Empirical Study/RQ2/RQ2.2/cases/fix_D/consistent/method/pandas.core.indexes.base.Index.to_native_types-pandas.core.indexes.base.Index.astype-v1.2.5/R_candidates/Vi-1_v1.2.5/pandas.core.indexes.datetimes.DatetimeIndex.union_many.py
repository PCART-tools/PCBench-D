    def union_many(self, others):
        """
        A bit of a hack to accelerate unioning a collection of indexes.
        """
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

            if this._can_fast_union(other):
                this = this._fast_union(other)
            else:
                this = Index.union(this, other)

        res_name = get_unanimous_names(self, *others)[0]
        if this.name != res_name:
            return this.rename(res_name)
        return this
