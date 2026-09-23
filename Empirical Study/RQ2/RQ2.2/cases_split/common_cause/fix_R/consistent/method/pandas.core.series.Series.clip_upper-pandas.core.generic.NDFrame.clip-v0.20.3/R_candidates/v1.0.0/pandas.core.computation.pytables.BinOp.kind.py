    @property
    def kind(self):
        """ the kind of my field """
        return getattr(self.queryables.get(self.lhs), "kind", None)
