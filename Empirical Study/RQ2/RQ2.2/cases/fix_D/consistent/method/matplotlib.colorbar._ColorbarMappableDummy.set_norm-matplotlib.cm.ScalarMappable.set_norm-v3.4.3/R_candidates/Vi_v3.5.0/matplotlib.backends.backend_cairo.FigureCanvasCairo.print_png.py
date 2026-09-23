    @_check_savefig_extra_args
    def print_png(self, fobj):
        self._get_printed_image_surface().write_to_png(fobj)
