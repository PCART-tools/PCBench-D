    def get_window_title(self):
        """
        Return the title text of the window containing the figure, or None
        if there is no window (e.g., a PS backend).
        """
        if self.manager is not None:
            return self.manager.get_window_title()
