    @_check_savefig_extra_args
    def print_rgba(self, fobj):
        width, height = self.get_width_height()
        buf = self._get_printed_image_surface().get_data()
        fobj.write(cbook._premultiplied_argb32_to_unmultiplied_rgba8888(
            np.asarray(buf).reshape((width, height, 4))))
