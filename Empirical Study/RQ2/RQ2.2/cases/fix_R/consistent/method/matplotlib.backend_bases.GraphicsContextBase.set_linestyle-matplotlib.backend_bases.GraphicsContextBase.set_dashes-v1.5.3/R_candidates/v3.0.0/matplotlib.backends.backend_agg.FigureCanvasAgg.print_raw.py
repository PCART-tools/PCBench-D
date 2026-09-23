    def print_raw(self, filename_or_obj, *args, **kwargs):
        FigureCanvasAgg.draw(self)
        renderer = self.get_renderer()
        with cbook._setattr_cm(renderer, dpi=self.figure.dpi), \
                cbook.open_file_cm(filename_or_obj, "wb") as fh:
            fh.write(renderer._renderer.buffer_rgba())
