    def print_raw(self, filename_or_obj, *, metadata=None):
        if metadata is not None:
            raise ValueError("metadata not supported for raw/rgba")
        FigureCanvasAgg.draw(self)
        renderer = self.get_renderer()
        with cbook.open_file_cm(filename_or_obj, "wb") as fh:
            fh.write(renderer.buffer_rgba())
