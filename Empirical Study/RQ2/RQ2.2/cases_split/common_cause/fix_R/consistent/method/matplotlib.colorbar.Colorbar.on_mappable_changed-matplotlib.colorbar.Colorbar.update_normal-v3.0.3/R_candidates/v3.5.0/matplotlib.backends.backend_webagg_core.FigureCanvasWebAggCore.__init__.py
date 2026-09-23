    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set to True when the renderer contains data that is newer
        # than the PNG buffer.
        self._png_is_old = True

        # Set to True by the `refresh` message so that the next frame
        # sent to the clients will be a full frame.
        self._force_full = True

        # Store the current image mode so that at any point, clients can
        # request the information. This should be changed by calling
        # self.set_image_mode(mode) so that the notification can be given
        # to the connected clients.
        self._current_image_mode = 'full'
