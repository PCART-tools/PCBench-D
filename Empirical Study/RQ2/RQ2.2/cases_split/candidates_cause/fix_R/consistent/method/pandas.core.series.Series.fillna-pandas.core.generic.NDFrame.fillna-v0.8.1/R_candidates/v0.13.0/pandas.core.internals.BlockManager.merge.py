    def merge(self, other, lsuffix=None, rsuffix=None):
        if not self._is_indexed_like(other):
            raise AssertionError('Must have same axes to merge managers')

        this, other = self._maybe_rename_join(other, lsuffix, rsuffix)

        cons_items = this.items + other.items
        new_axes = list(this.axes)
        new_axes[0] = cons_items

        consolidated = _consolidate(this.blocks + other.blocks, cons_items)
        return self.__class__(consolidated, new_axes)
