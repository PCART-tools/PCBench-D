    def remove(self):
        """
        Overload the remove method
        """
        # disconnect the call back
        self.ax.figure.callbacks.disconnect(self._cid)
        self._cid = None
        # pass the remove call up the stack
        mcollections.PolyCollection.remove(self)
