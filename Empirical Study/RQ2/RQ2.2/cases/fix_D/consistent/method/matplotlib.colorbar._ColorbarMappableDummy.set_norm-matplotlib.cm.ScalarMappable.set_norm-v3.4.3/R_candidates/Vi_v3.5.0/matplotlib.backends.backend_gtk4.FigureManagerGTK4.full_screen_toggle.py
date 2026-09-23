    def full_screen_toggle(self):
        if not self.window.is_fullscreen():
            self.window.fullscreen()
        else:
            self.window.unfullscreen()
