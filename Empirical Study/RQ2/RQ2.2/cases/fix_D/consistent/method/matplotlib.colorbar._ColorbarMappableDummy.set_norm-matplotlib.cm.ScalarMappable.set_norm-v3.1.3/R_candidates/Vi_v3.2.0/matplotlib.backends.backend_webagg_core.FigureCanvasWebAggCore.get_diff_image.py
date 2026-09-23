    def get_diff_image(self):
        if self._png_is_old:
            renderer = self.get_renderer()

            # The buffer is created as type uint32 so that entire
            # pixels can be compared in one numpy call, rather than
            # needing to compare each plane separately.
            buff = (np.frombuffer(renderer.buffer_rgba(), dtype=np.uint32)
                    .reshape((renderer.height, renderer.width)))

            # If any pixels have transparency, we need to force a full
            # draw as we cannot overlay new on top of old.
            pixels = buff.view(dtype=np.uint8).reshape(buff.shape + (4,))

            if self._force_full or np.any(pixels[:, :, 3] != 255):
                self.set_image_mode('full')
                output = buff
            else:
                self.set_image_mode('diff')
                last_buffer = (np.frombuffer(self._last_renderer.buffer_rgba(),
                                             dtype=np.uint32)
                               .reshape((renderer.height, renderer.width)))
                diff = buff != last_buffer
                output = np.where(diff, buff, 0)

            # TODO: We should write a new version of write_png that
            # handles the differencing inline
            buff = _png.write_png(
                output.view(dtype=np.uint8).reshape(output.shape + (4,)),
                None, compression=6, filter=_png.PNG_FILTER_NONE)

            # Swap the renderer frames
            self._renderer, self._last_renderer = (
                self._last_renderer, renderer)
            self._force_full = False
            self._png_is_old = False
            return buff
