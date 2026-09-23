    def print_png(self, filename_or_obj, *args, **kwargs):
        FigureCanvasAgg.draw(self)
        renderer = self.get_renderer()
        original_dpi = renderer.dpi
        renderer.dpi = self.figure.dpi
        if isinstance(filename_or_obj, six.string_types):
            filename_or_obj = open(filename_or_obj, 'wb')
            close = True
        else:
            close = False

        version_str = 'matplotlib version ' + __version__ + \
            ', http://matplotlib.org/'
        metadata = OrderedDict({'Software': version_str})
        user_metadata = kwargs.pop("metadata", None)
        if user_metadata is not None:
            metadata.update(user_metadata)

        try:
            _png.write_png(renderer._renderer, filename_or_obj,
                           self.figure.dpi, metadata=metadata)
        finally:
            if close:
                filename_or_obj.close()
            renderer.dpi = original_dpi
