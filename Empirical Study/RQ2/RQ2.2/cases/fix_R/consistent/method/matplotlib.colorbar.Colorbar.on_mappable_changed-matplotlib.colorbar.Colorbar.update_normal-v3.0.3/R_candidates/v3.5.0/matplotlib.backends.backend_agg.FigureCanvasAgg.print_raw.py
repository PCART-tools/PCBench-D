    @_check_savefig_extra_args
    @_api.delete_parameter("3.5", "args")
    def print_raw(self, filename_or_obj, *args):
        FigureCanvasAgg.draw(self)
        renderer = self.get_renderer()
        with cbook.open_file_cm(filename_or_obj, "wb") as fh:
            fh.write(renderer.buffer_rgba())
