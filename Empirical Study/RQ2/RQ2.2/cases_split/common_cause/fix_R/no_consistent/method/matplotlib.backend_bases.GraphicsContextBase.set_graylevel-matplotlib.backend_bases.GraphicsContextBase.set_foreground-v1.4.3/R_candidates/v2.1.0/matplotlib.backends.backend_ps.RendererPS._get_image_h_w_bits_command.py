    def _get_image_h_w_bits_command(self, im):
        h, w, bits = self._rgb(im)
        imagecmd = "false 3 colorimage"

        return h, w, bits, imagecmd
