    @_check_savefig_extra_args()
    @_api.delete_parameter("3.5", "args")
    def print_jpg(self, filename_or_obj, *args, pil_kwargs=None, **kwargs):
        """
        Write the figure to a JPEG file.

        Parameters
        ----------
        filename_or_obj : str or path-like or file-like
            The file to write to.

        Other Parameters
        ----------------
        pil_kwargs : dict, optional
            Additional keyword arguments that are passed to
            `PIL.Image.Image.save` when saving the figure.
        """
        # Remove transparency by alpha-blending on an assumed white background.
        r, g, b, a = mcolors.to_rgba(self.figure.get_facecolor())
        try:
            self.figure.set_facecolor(a * np.array([r, g, b]) + 1 - a)
            FigureCanvasAgg.draw(self)
        finally:
            self.figure.set_facecolor((r, g, b, a))
        if pil_kwargs is None:
            pil_kwargs = {}
        pil_kwargs.setdefault("dpi", (self.figure.dpi, self.figure.dpi))
        # Drop alpha channel now.
        return (Image.fromarray(np.asarray(self.buffer_rgba())[..., :3])
                .save(filename_or_obj, format='jpeg', **pil_kwargs))
