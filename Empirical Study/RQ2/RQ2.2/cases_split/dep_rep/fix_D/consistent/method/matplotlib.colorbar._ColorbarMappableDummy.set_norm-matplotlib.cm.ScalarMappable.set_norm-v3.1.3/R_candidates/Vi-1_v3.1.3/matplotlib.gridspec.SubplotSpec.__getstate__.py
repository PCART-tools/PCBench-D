    def __getstate__(self):
        state = self.__dict__
        try:
            state.pop('_layoutbox')
        except KeyError:
            pass
        return state
