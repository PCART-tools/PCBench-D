    def pan(self, *args):
        super().pan(*args)
        self._update_buttons_checked()
