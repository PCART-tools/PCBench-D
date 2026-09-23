    def rename_axis(self, mapper, axis=1):

        index = self.axes[axis]
        if isinstance(index, MultiIndex):
            new_axis = MultiIndex.from_tuples(
                [tuple(mapper(y) for y in x) for x in index],
                names=index.names)
        else:
            new_axis = Index([mapper(x) for x in index], name=index.name)

        if not new_axis.is_unique:
            raise AssertionError('New axis must be unique to rename')

        new_axes = list(self.axes)
        new_axes[axis] = new_axis
        return self.__class__(self.blocks, new_axes)
