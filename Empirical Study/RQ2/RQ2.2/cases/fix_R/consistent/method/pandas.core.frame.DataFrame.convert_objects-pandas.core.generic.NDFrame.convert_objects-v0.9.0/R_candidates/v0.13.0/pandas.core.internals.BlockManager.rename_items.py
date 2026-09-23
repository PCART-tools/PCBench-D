    def rename_items(self, mapper, copy=True):
        if isinstance(self.items, MultiIndex):
            items = [tuple(mapper(y) for y in x) for x in self.items]
            new_items = MultiIndex.from_tuples(items, names=self.items.names)
        else:
            items = [mapper(x) for x in self.items]
            new_items = Index(items, name=self.items.name)

        new_blocks = []
        for block in self.blocks:
            newb = block.copy(deep=copy)
            newb.set_ref_items(new_items, maybe_rename=True)
            new_blocks.append(newb)
        new_axes = list(self.axes)
        new_axes[0] = new_items
        return self.__class__(new_blocks, new_axes)
