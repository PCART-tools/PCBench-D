class _ValuesView(abc.KeysView):

    def __init__(self, mapping, *, getall=False):
        super().__init__(mapping)
        self._getall = getall

    def __contains__(self, value):
        for values in self._mapping.values():
            if self._getall and value in values:
                return True
            elif value == values[0]:
                return True
        return False

    def __iter__(self):
        for values in self._mapping.values():
            if self._getall:
                yield from iter(values)
            else:
                yield values[0]
