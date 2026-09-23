    def disconnect(self, cid):
        """Remove the callback function with connection id *cid*."""
        self._observers.disconnect(cid)
