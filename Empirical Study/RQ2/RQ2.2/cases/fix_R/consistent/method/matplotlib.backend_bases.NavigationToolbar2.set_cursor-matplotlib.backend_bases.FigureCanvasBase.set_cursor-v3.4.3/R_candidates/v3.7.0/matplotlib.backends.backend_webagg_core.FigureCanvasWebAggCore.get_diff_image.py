    def get_diff_image(self):
        if self._png_is_old:
            renderer = self.get_renderer()

            pixels = np.asarray(renderer.buffer_rgba())
            # The buffer is created as type uint32 so that entire
            # pixels can be compared in one numpy call, rather than
            # needing to compare each plane separately.
            buff = pixels.view(np.uint32).squeeze(2)

            if (self._force_full
                    # If the buffer has changed size we need to do a full draw.
                    or buff.shape != self._last_buff.shape
                    # If any pixels have transparency, we need to force a full
                    # draw as we cannot overlay new on top of old.
                    or (pixels[:, :, 3] != 255).any()):
                self.set_image_mode('full')
                output = buff
            else:
                self.set_image_mode('diff')
                diff = buff != self._last_buff
                output = np.where(diff, buff, 0)

            # Store the current buffer so we can compute the next diff.
            self._last_buff = buff.copy()
            self._force_full = False
            self._png_is_old = False

            data = output.view(dtype=np.uint8).reshape((*output.shape, 4))
            with BytesIO() as png:
                Image.fromarray(data).save(png, format="png")
                return png.getvalue()
