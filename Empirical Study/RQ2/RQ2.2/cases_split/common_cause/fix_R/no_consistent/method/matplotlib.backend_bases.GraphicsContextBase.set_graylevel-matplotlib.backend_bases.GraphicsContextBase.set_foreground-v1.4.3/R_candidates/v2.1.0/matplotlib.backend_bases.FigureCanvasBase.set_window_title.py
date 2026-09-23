    def set_window_title(self, title):
        """
        Set the title text of the window containing the figure.  Note that
        this has no effect if there is no window (e.g., a PS backend).
        """
        if hasattr(self, "manager"):
            self.manager.set_window_title(title)
