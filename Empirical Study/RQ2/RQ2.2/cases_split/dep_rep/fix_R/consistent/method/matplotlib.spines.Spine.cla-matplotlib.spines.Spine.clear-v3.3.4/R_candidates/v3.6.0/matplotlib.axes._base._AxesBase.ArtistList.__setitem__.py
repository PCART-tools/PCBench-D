        def __setitem__(self, key, item):
            _api.warn_deprecated(
                '3.5',
                name=f'modification of the Axes.{self._prop_name}',
                obj_type='property',
                alternative=f'Artist.remove() and Axes.f{self._add_name}')
            del self[key]
            if isinstance(key, slice):
                key = key.start
            if not np.iterable(item):
                self.insert(key, item)
                return

            try:
                index = self._axes._children.index(self[key])
            except IndexError:
                index = None
            for i, artist in enumerate(item):
                getattr(self._axes, self._add_name)(artist)
            if index is not None:
                # Move new items to the specified index, if there's something
                # to put it before.
                i = -(i + 1)
                self._axes._children[index:index] = self._axes._children[i:]
                del self._axes._children[i:]
