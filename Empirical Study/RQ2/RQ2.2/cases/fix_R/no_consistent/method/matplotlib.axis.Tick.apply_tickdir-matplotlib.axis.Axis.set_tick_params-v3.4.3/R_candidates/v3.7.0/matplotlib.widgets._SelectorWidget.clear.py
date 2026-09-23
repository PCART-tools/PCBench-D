    def clear(self):
        """Clear the selection and set the selector ready to make a new one."""
        self._clear_without_update()
        self.update()
