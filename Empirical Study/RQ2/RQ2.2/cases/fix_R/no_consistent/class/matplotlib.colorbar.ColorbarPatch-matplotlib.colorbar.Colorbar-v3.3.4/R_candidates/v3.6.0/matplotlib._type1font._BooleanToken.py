class _BooleanToken(_Token):
    kind = 'boolean'

    def value(self):
        return self.raw == 'true'
