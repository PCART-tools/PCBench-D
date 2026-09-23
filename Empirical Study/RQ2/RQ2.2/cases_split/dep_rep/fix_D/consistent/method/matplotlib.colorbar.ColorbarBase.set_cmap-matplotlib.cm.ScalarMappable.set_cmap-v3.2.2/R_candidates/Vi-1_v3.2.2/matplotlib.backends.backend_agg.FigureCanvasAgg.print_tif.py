        @cbook._delete_parameter("3.2", "dryrun")
        def print_tif(self, filename_or_obj, *args, dryrun=False,
                      pil_kwargs=None, **kwargs):
            FigureCanvasAgg.draw(self)
            if dryrun:
                return
            if pil_kwargs is None:
                pil_kwargs = {}
            pil_kwargs.setdefault("dpi", (self.figure.dpi, self.figure.dpi))
            return (Image.fromarray(np.asarray(self.buffer_rgba()))
                    .save(filename_or_obj, format='tiff', **pil_kwargs))
