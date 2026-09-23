    def print_png(self, fobj, *args, **kwargs):
        self._get_printed_image_surface().write_to_png(fobj)
