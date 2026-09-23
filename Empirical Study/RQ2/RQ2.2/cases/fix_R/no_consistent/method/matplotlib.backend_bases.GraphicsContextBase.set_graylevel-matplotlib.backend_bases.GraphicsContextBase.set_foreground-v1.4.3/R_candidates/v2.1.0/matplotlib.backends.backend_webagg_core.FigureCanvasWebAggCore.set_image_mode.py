    def set_image_mode(self, mode):
        """
        Set the image mode for any subsequent images which will be sent
        to the clients. The modes may currently be either 'full' or 'diff'.

        Note: diff images may not contain transparency, therefore upon
        draw this mode may be changed if the resulting image has any
        transparent component.

        """
        if mode not in ['full', 'diff']:
            raise ValueError('image mode must be either full or diff.')
        if self._current_image_mode != mode:
            self._current_image_mode = mode
            self.handle_send_image_mode(None)
