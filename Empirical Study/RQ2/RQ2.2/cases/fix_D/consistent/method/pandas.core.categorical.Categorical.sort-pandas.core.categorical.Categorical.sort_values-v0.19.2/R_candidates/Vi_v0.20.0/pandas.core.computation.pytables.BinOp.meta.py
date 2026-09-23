    @property
    def meta(self):
        """ the meta of my field """
        return getattr(self.queryables.get(self.lhs), 'meta', None)
