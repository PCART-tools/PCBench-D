    def disconnect(self, cid):
        """Remove the observer with connection id *cid*."""
        try:
            del self.observers[cid]
        except KeyError:
            pass
