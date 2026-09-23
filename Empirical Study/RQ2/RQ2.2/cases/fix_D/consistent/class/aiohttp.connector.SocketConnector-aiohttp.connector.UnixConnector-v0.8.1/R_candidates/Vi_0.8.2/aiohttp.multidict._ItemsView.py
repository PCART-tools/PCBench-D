class _ItemsView(abc.ItemsView):

    def __init__(self, mapping, *, getall=False):
        super().__init__(mapping)
        self._getall = getall

    def __contains__(self, item):
        key, value = item
        try:
            values = self._mapping[key]
        except KeyError:
            return False
        else:
            if self._getall:
                return value in values
            else:
                return value == values[0]

    def __iter__(self):
        for key, values in self._mapping.items():
            if self._getall:
                for value in values:
                    yield key, value
            else:
                yield key, values[0]
