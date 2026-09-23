    def clear(self):
        """Clear the selection and set the selector ready to make a new one."""
        self._selection_completed = False
        self.set_visible(False)
        self.update()
