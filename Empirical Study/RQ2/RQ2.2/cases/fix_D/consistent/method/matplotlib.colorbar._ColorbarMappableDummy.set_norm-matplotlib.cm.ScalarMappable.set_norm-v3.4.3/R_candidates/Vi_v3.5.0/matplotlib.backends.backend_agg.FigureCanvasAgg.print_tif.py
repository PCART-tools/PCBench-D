    @_check_savefig_extra_args
    def print_tif(self, filename_or_obj, *, pil_kwargs=None):
        FigureCanvasAgg.draw(self)
        if pil_kwargs is None:
            pil_kwargs = {}
        pil_kwargs.setdefault("dpi", (self.figure.dpi, self.figure.dpi))
        return (Image.fromarray(np.asarray(self.buffer_rgba()))
                .save(filename_or_obj, format='tiff', **pil_kwargs))
