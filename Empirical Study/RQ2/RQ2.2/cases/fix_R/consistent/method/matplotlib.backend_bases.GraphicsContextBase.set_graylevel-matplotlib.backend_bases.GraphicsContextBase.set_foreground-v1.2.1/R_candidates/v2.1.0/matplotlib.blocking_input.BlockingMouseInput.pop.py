    def pop(self, event, index=-1):
        """
        This removes a click and the associated event from the object.
        Defaults to removing the last click, but any index can be
        supplied.
        """
        self.pop_click(event, index)
        BlockingInput.pop(self, index)
