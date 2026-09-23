    def pop(self, event, index=-1):
        """
        Remove a click and the associated event from the list of clicks.

        Defaults to the last click.
        """
        self.pop_click(event, index)
        BlockingInput.pop(self, index)
