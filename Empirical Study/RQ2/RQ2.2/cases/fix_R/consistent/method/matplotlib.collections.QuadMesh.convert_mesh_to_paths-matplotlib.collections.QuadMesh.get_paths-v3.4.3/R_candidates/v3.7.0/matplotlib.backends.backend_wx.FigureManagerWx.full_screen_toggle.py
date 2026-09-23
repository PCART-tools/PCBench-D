    def full_screen_toggle(self):
        # docstring inherited
        self.frame.ShowFullScreen(not self.frame.IsFullScreen())
