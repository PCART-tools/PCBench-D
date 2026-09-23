    def __setstate__(self, state):
        next_counter = state.pop('_counter')
        vars(self).update(state)
        self._counter = itertools.count(next_counter)
