    def _pixmap_prepare(self, width, height):
        """
        Make sure _._pixmap is at least width, height,
        create new pixmap if necessary
        """
        create_pixmap = False
        if width > self._pixmap_width:
            # increase the pixmap in 10%+ (rather than 1 pixel) steps
            self._pixmap_width  = max (int (self._pixmap_width  * 1.1),
                                       width)
            create_pixmap = True

        if height > self._pixmap_height:
            self._pixmap_height = max (int (self._pixmap_height * 1.1),
                                           height)
            create_pixmap = True

        if create_pixmap:
            self._pixmap = gdk.Pixmap (self.window, self._pixmap_width,
                                       self._pixmap_height)
            self._renderer.set_pixmap (self._pixmap)
