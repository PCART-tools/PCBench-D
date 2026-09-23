class MutableMultiDict(abc.MutableMapping, MultiDict):
    """An ordered dictionary that can have multiple values for each key."""

    def getall(self, key):
        """Returns all values stored at key as list.

        Raises KeyError if key doesn't exist.
        """
        return list(self._items[key])

    def add(self, key, value):
        """Adds value to a key."""
        if key in self._items:
            self._items[key].append(value)
        else:
            self._items[key] = [value]

    def extend(self, *args, **kwargs):
        """Extends current MutableMultiDict with more values.

        This method must be used instead of update.
        """
        if len(args) > 1:
            raise TypeError("extend takes at most 2 positional arguments"
                            " ({} given)".format(len(args) + 1))
        if args:
            if isinstance(args[0], MultiDict):
                items = args[0].items(getall=True)
            elif hasattr(args[0], 'items'):
                items = args[0].items()
            else:
                items = args[0]
        else:
            items = []
        for key, value in chain(items, kwargs.items()):
            self.add(key, value)

    def clear(self):
        """Remove all items from MutableMultiDict"""
        self._items.clear()

    # MutableMapping interface #

    def __setitem__(self, key, value):
        self._items[key] = [value]

    def __delitem__(self, key):
        del self._items[key]

    def pop(self, key, default=None):
        """Method not allowed."""
        raise NotImplementedError

    def popitem(self):
        """Method not allowed."""
        raise NotImplementedError

    def update(self, *args, **kw):
        """Method not allowed."""
        raise NotImplementedError("Use extend method instead")
