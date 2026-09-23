    def __repr__(self):
        return '<Signal owner={}, frozen={}, {!r}>'.format(self._owner,
                                                           self.frozen,
                                                           list(self))
