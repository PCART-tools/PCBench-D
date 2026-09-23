    def on_text_change(self, func):
        """
        When the text changes, call this *func* with event.

        A connection id is returned which can be used to disconnect.
        """
        cid = self.cnt
        self.change_observers[cid] = func
        self.cnt += 1
        return cid
