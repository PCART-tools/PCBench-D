class _NameToken(_Token):
    kind = 'name'

    def is_slash_name(self):
        return self.raw.startswith('/')

    def value(self):
        return self.raw[1:]
