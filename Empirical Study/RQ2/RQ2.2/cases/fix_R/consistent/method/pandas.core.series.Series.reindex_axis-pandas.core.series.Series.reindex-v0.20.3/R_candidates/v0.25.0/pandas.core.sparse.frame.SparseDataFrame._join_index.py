    def _join_index(self, other, how, lsuffix, rsuffix):
        if isinstance(other, Series):
            if other.name is None:
                raise ValueError("Other Series must have a name")

            other = SparseDataFrame(
                {other.name: other}, default_fill_value=self._default_fill_value
            )

        join_index = self.index.join(other.index, how=how)

        this = self.reindex(join_index)
        other = other.reindex(join_index)

        this, other = this._maybe_rename_join(other, lsuffix, rsuffix)

        from pandas import concat

        return concat([this, other], axis=1, verify_integrity=True)
