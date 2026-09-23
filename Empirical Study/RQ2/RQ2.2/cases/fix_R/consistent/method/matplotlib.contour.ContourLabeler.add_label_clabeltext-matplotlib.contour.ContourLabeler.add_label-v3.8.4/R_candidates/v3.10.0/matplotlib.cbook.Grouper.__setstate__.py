    def __setstate__(self, state):
        vars(self).update(state)
        # Convert strong refs to weak ones.
        self._mapping = weakref.WeakKeyDictionary(
            {k: weakref.WeakSet(v) for k, v in self._mapping.items()})
        self._ordering = weakref.WeakKeyDictionary(self._ordering)
