    def remove(self):
        # docstring inherited
        self.axes.figure.callbacks.disconnect(self._cid)
        self._cid = None
        super().remove()  # pass the remove call up the stack
