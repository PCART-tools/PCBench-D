    def disconnect(self, cid):
        """
        Remove the observer with connection id *cid*

        Parameters
        ----------
        cid : int
            Connection id of the observer to be removed
        """
        try:
            del self.observers[cid]
        except KeyError:
            pass
