    def on_clicked(self, func):
        """
        Connect the callback function *func* to button click events.

        Returns a connection id, which can be used to disconnect the callback.
        """
        cid = self.cnt
        self.observers[cid] = func
        self.cnt += 1
        return cid
