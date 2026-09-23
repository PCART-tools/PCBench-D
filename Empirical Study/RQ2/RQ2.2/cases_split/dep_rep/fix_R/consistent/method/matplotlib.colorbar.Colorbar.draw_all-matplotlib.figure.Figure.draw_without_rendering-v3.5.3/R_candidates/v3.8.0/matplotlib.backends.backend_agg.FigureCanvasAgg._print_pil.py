    def _print_pil(self, filename_or_obj, fmt, pil_kwargs, metadata=None):
        """
        Draw the canvas, then save it using `.image.imsave` (to which
        *pil_kwargs* and *metadata* are forwarded).
        """
        FigureCanvasAgg.draw(self)
        mpl.image.imsave(
            filename_or_obj, self.buffer_rgba(), format=fmt, origin="upper",
            dpi=self.figure.dpi, metadata=metadata, pil_kwargs=pil_kwargs)
