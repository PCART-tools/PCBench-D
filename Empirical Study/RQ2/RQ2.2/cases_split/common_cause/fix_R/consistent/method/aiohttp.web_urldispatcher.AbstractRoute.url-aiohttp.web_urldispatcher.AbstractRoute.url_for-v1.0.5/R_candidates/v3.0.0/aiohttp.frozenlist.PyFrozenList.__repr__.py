    def __repr__(self):
        return '<FrozenList(frozen={}, {!r})>'.format(self._frozen,
                                                      self._items)
