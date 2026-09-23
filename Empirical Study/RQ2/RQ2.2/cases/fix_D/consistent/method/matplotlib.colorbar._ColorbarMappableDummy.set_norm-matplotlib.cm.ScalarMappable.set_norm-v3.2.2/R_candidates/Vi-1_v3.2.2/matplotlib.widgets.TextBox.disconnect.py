    def disconnect(self, cid):
        """Remove the observer with connection id *cid*."""
        for reg in [self.change_observers, self.submit_observers]:
            try:
                del reg[cid]
            except KeyError:
                pass
