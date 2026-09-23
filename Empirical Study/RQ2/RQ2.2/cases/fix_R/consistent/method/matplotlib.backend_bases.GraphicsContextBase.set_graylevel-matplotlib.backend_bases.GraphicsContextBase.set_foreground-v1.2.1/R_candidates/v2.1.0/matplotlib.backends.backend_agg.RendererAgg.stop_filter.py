    def stop_filter(self, post_processing):
        """
        Save the plot in the current canvas as a image and apply
        the *post_processing* function.

           def post_processing(image, dpi):
             # ny, nx, depth = image.shape
             # image (numpy array) has RGBA channels and has a depth of 4.
             ...
             # create a new_image (numpy array of 4 channels, size can be
             # different). The resulting image may have offsets from
             # lower-left corner of the original image
             return new_image, offset_x, offset_y

        The saved renderer is restored and the returned image from
        post_processing is plotted (using draw_image) on it.
        """

        # WARNING.
        # For agg_filter to work, the rendere's method need
        # to overridden in the class. See draw_markers, and draw_path_collections

        width, height = int(self.width), int(self.height)

        buffer, bounds = self.tostring_rgba_minimized()

        l, b, w, h = bounds

        self._renderer = self._filter_renderers.pop()
        self._update_methods()

        if w > 0 and h > 0:
            img = np.fromstring(buffer, np.uint8)
            img, ox, oy = post_processing(img.reshape((h, w, 4)) / 255.,
                                          self.dpi)
            gc = self.new_gc()
            if img.dtype.kind == 'f':
                img = np.asarray(img * 255., np.uint8)
            img = img[::-1]
            self._renderer.draw_image(
                gc, l + ox, height - b - h + oy, img)
