    def on_clicked(self, func):
        """
        When the button is clicked, call this *func* with event.

        A connection id is returned. It can be used to disconnect
        the button from its callback.
        """
        cid = self.cnt
        self.observers[cid] = func
        self.cnt += 1
        return cid
