    @_check_savefig_extra_args(
        extra_kwargs=["quality", "optimize", "progressive"])
    @cbook._delete_parameter("3.2", "dryrun")
    @cbook._delete_parameter("3.3", "quality",
                             alternative="pil_kwargs={'quality': ...}")
    @cbook._delete_parameter("3.3", "optimize",
                             alternative="pil_kwargs={'optimize': ...}")
    @cbook._delete_parameter("3.3", "progressive",
                             alternative="pil_kwargs={'progressive': ...}")
    def print_jpg(self, filename_or_obj, *args, dryrun=False, pil_kwargs=None,
                  **kwargs):
        """
        Write the figure to a JPEG file.

        Parameters
        ----------
        filename_or_obj : str or path-like or file-like
            The file to write to.

        Other Parameters
        ----------------
        quality : int, default: :rc:`savefig.jpeg_quality`
            The image quality, on a scale from 1 (worst) to 95 (best).
            Values above 95 should be avoided; 100 disables portions of
            the JPEG compression algorithm, and results in large files
            with hardly any gain in image quality.  This parameter is
            deprecated.

        optimize : bool, default: False
            Whether the encoder should make an extra pass over the image
            in order to select optimal encoder settings.  This parameter is
            deprecated.

        progressive : bool, default: False
            Whether the image should be stored as a progressive JPEG file.
            This parameter is deprecated.

        pil_kwargs : dict, optional
            Additional keyword arguments that are passed to
            `PIL.Image.Image.save` when saving the figure.  These take
            precedence over *quality*, *optimize* and *progressive*.
        """
        # Remove transparency by alpha-blending on an assumed white background.
        r, g, b, a = mcolors.to_rgba(self.figure.get_facecolor())
        try:
            self.figure.set_facecolor(a * np.array([r, g, b]) + 1 - a)
            FigureCanvasAgg.draw(self)
        finally:
            self.figure.set_facecolor((r, g, b, a))
        if dryrun:
            return
        if pil_kwargs is None:
            pil_kwargs = {}
        for k in ["quality", "optimize", "progressive"]:
            if k in kwargs:
                pil_kwargs.setdefault(k, kwargs.pop(k))
        if "quality" not in pil_kwargs:
            quality = pil_kwargs["quality"] = \
                dict.__getitem__(mpl.rcParams, "savefig.jpeg_quality")
            if quality not in [0, 75, 95]:  # default qualities.
                cbook.warn_deprecated(
                    "3.3", name="savefig.jpeg_quality", obj_type="rcParam",
                    addendum="Set the quality using "
                    "`pil_kwargs={'quality': ...}`; the future default "
                    "quality will be 75, matching the default of Pillow and "
                    "libjpeg.")
        pil_kwargs.setdefault("dpi", (self.figure.dpi, self.figure.dpi))
        # Drop alpha channel now.
        return (Image.fromarray(np.asarray(self.buffer_rgba())[..., :3])
                .save(filename_or_obj, format='jpeg', **pil_kwargs))
