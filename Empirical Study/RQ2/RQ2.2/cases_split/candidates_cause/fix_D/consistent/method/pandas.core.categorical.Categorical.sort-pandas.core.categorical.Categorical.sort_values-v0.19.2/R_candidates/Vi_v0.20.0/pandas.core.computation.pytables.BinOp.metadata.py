    @property
    def metadata(self):
        """ the metadata of my field """
        return getattr(self.queryables.get(self.lhs), 'metadata', None)
