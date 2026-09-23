class MultiDict(abc.Mapping):
    """Read-only ordered dictionary that can hava multiple values for each key.

    This type of MultiDict must be used for request headers and query args.
    """

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("MultiDict takes at most 2 positional "
                            "arguments ({} given)".format(len(args) + 1))
        self._items = OrderedDict()
        if args:
            if hasattr(args[0], 'items'):
                args = list(args[0].items())
            else:
                args = list(args[0])

        for key, value in chain(args, kwargs.items()):
            if key in self._items:
                self._items[key].append(value)
            else:
                self._items[key] = [value]

    def get(self, key, default=None):
        """Return first value stored at key."""
        if key in self._items and self._items[key]:
            return self._items[key][0]
        else:
            return default

    def getall(self, key):
        """Returns all values stored at key as a tuple.

        Raises KeyError if key doesn't exist."""
        return tuple(self._items[key])

    def getone(self, key):
        """Return first value stored at key."""
        return self._items[key][0]

    # extra methods #

    def copy(self):
        """Returns a copy itself."""
        cls = self.__class__
        return cls(self.items(getall=True))

    # Mapping interface #

    def __getitem__(self, key):
        return self._items[key][0]

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def items(self, *, getall=False):
        return _ItemsView(self._items, getall=getall)

    def values(self, *, getall=False):
        return _ValuesView(self._items, getall=getall)

    def __eq__(self, other):
        if not isinstance(other, abc.Mapping):
            return NotImplemented
        if isinstance(other, MultiDict):
            return self._items == other._items
        return dict(self.items()) == dict(other.items())

    def __contains__(self, key):
        return key in self._items

    def __repr__(self):
        return '<{} {!r}>'.format(self.__class__.__name__, self._items)
