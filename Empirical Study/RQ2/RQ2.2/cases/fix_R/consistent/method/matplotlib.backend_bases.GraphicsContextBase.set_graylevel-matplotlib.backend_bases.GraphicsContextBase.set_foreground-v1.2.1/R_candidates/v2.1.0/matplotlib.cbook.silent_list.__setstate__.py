    def __setstate__(self, state):
        self.type = state['type']
        self.extend(state['seq'])
