    def stop_rasterizing(self):
        """
        Exit "raster" mode.  All of the drawing that was done since
        the last `start_rasterizing` call will be copied to the
        vector backend by calling draw_image.

        If `start_rasterizing` has been called multiple times,
        `stop_rasterizing` must be called the same number of times before
        "raster" mode is exited.
        """
        self._rasterizing -= 1
        if self._rasterizing == 0:
            self._renderer = self._vector_renderer

            height = self._height * self.dpi
            buffer, bounds = self._raster_renderer.tostring_rgba_minimized()
            l, b, w, h = bounds
            if w > 0 and h > 0:
                image = np.frombuffer(buffer, dtype=np.uint8)
                image = image.reshape((h, w, 4))
                image = image[::-1]
                gc = self._renderer.new_gc()
                # TODO: If the mixedmode resolution differs from the figure's
                #       dpi, the image must be scaled (dpi->_figdpi). Not all
                #       backends support this.
                self._renderer.draw_image(
                    gc,
                    l * self._figdpi / self.dpi,
                    (height-b-h) * self._figdpi / self.dpi,
                    image)
            self._raster_renderer = None
            self._rasterizing = False

            # restore the figure dpi.
            self.figure.set_dpi(self._figdpi)

        if self._bbox_inches_restore:  # when tight bbox is used
            r = process_figure_for_rasterizing(self.figure,
                                               self._bbox_inches_restore,
                                               self._figdpi)
            self._bbox_inches_restore = r
