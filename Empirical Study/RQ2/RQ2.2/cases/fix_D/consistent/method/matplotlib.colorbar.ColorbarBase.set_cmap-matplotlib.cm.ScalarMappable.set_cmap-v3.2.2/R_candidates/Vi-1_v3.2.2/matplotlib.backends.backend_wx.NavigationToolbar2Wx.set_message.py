    def set_message(self, s):
        status_bar = self.GetTopLevelParent().GetStatusBar()
        if status_bar is not None and hasattr(status_bar, 'set_function'):
            status_bar.set_function(s)
