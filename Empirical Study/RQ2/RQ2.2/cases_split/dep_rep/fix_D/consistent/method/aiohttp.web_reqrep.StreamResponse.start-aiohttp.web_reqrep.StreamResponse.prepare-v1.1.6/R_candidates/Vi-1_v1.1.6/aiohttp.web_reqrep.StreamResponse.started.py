    @property
    def started(self):
        warnings.warn('use Response.prepared instead', DeprecationWarning)
        return self.prepared
