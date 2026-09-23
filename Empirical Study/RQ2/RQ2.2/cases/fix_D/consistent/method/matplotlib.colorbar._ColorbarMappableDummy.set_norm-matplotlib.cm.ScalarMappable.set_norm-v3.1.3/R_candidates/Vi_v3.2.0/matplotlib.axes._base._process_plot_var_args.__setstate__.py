    def __setstate__(self, state):
        self.__dict__ = state.copy()
        self.set_prop_cycle()
