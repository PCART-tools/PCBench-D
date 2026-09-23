    def full_screen_toggle(self):
        is_fullscreen = {
            3: lambda w: (w.get_window().get_state()
                          & Gdk.WindowState.FULLSCREEN),
            4: lambda w: w.is_fullscreen(),
        }[self._gtk_ver]
        if is_fullscreen(self.window):
            self.window.unfullscreen()
        else:
            self.window.fullscreen()
