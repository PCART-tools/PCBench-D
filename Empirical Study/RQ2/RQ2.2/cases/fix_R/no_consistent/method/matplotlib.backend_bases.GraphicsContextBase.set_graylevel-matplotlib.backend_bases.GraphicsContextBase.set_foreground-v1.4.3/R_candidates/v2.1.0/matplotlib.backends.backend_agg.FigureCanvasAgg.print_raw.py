    def print_raw(self, filename_or_obj, *args, **kwargs):
        FigureCanvasAgg.draw(self)
        renderer = self.get_renderer()
        original_dpi = renderer.dpi
        renderer.dpi = self.figure.dpi
        if isinstance(filename_or_obj, six.string_types):
            fileobj = open(filename_or_obj, 'wb')
            close = True
        else:
            fileobj = filename_or_obj
            close = False
        try:
            fileobj.write(renderer._renderer.buffer_rgba())
        finally:
            if close:
                fileobj.close()
            renderer.dpi = original_dpi
