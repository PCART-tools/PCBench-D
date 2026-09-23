    def __getattr__(self, id):
        """Calculate missing attribute"""
        if id[:4] == "_get":
            raise AttributeError(id)
        # calculate missing attribute
        v = getattr(self, "_get" + id)()
        setattr(self, id, v)
        return v
