        def insert(self, index, item):
            _api.warn_deprecated(
                '3.5',
                name=f'modification of the Axes.{self._prop_name}',
                obj_type='property',
                alternative=f'Axes.{self._add_name}')
            try:
                index = self._axes._children.index(self[index])
            except IndexError:
                index = None
            getattr(self._axes, self._add_name)(item)
            if index is not None:
                # Move new item to the specified index, if there's something to
                # put it before.
                self._axes._children[index:index] = self._axes._children[-1:]
                del self._axes._children[-1]
