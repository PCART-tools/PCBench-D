    def __repr__(self):
        return "<{} {}>".format(
            self.__class__.__name__,
            'connected' if self.transport is not None else 'disconnected')
