    def zoom(self, *args):
        super().zoom(*args)
        self._update_buttons_checked()
