    def handle_send_image_mode(self, event):
        # The client requests notification of what the current image mode is.
        self.send_event('image_mode', mode=self._current_image_mode)
