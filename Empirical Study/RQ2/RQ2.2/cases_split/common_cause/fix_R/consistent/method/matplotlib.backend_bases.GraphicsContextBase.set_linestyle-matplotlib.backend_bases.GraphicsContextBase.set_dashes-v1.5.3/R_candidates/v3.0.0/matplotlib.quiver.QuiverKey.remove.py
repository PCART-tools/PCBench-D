    def remove(self):
        """
        Overload the remove method
        """
        self.Q.ax.figure.callbacks.disconnect(self._cid)
        self._cid = None
        # pass the remove call up the stack
        martist.Artist.remove(self)
