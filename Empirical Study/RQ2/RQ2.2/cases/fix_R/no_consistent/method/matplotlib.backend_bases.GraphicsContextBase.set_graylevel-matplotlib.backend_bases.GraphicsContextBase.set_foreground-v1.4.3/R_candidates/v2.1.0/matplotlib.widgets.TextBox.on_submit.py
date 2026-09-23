    def on_submit(self, func):
        """
        When the user hits enter or leaves the submision box, call this
        *func* with event.

        A connection id is returned which can be used to disconnect.
        """
        cid = self.cnt
        self.submit_observers[cid] = func
        self.cnt += 1
        return cid
