    def get_window_title(self):
        """
        Get the title text of the window containing the figure.
        Return None if there is no window (e.g., a PS backend).
        """
        if hasattr(self, "manager"):
            return self.manager.get_window_title()
