    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop('related_model', None)
        return state
