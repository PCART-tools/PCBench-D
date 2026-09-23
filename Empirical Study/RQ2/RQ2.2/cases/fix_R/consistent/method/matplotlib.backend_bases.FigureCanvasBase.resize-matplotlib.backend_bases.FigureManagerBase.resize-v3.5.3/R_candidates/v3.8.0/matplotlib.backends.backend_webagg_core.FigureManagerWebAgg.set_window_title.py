    def set_window_title(self, title):
        self._send_event('figure_label', label=title)
        self._window_title = title
