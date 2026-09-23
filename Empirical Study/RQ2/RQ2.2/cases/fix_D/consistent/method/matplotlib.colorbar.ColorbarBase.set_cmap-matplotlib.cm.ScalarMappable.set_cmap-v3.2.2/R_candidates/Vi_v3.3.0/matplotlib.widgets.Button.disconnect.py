    def disconnect(self, cid):
        """Remove the callback function with connection id *cid*."""
        try:
            del self.observers[cid]
        except KeyError:
            pass
