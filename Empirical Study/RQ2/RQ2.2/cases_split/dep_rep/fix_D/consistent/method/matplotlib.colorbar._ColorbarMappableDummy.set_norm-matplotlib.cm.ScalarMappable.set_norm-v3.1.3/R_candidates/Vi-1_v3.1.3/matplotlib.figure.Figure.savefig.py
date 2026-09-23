    def savefig(self, fname, *, transparent=None, **kwargs):
        """
        Save the current figure.

        Call signature::

          savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                  orientation='portrait', papertype=None, format=None,
                  transparent=False, bbox_inches=None, pad_inches=0.1,
                  frameon=None, metadata=None)

        The output formats available depend on the backend being used.

        Parameters
        ----------

        fname : str or PathLike or file-like object
            A path, or a Python file-like object, or
            possibly some backend-dependent object such as
            `matplotlib.backends.backend_pdf.PdfPages`.

            If *format* is not set, then the output format is inferred from
            the extension of *fname*, if any, and from :rc:`savefig.format`
            otherwise.  If *format* is set, it determines the output format.

            Hence, if *fname* is not a path or has no extension, remember to
            specify *format* to ensure that the correct backend is used.

        Other Parameters
        ----------------

        dpi : [ *None* | scalar > 0 | 'figure' ]
            The resolution in dots per inch.  If *None*, defaults to
            :rc:`savefig.dpi`.  If 'figure', uses the figure's dpi value.

        quality : [ *None* | 1 <= scalar <= 100 ]
            The image quality, on a scale from 1 (worst) to 95 (best).
            Applicable only if *format* is jpg or jpeg, ignored otherwise.
            If *None*, defaults to :rc:`savefig.jpeg_quality` (95 by default).
            Values above 95 should be avoided; 100 completely disables the
            JPEG quantization stage.

        optimize : bool
            If *True*, indicates that the JPEG encoder should make an extra
            pass over the image in order to select optimal encoder settings.
            Applicable only if *format* is jpg or jpeg, ignored otherwise.
            Is *False* by default.

        progressive : bool
            If *True*, indicates that this image should be stored as a
            progressive JPEG file. Applicable only if *format* is jpg or
            jpeg, ignored otherwise. Is *False* by default.

        facecolor : color spec or None, optional
            The facecolor of the figure; if *None*, defaults to
            :rc:`savefig.facecolor`.

        edgecolor : color spec or None, optional
            The edgecolor of the figure; if *None*, defaults to
            :rc:`savefig.edgecolor`

        orientation : {'landscape', 'portrait'}
            Currently only supported by the postscript backend.

        papertype : str
            One of 'letter', 'legal', 'executive', 'ledger', 'a0' through
            'a10', 'b0' through 'b10'. Only supported for postscript
            output.

        format : str
            The file format, e.g. 'png', 'pdf', 'svg', ... The behavior when
            this is unset is documented under *fname*.

        transparent : bool
            If *True*, the axes patches will all be transparent; the
            figure patch will also be transparent unless facecolor
            and/or edgecolor are specified via kwargs.
            This is useful, for example, for displaying
            a plot on top of a colored background on a web page.  The
            transparency of these patches will be restored to their
            original values upon exit of this function.

        bbox_inches : str or `~matplotlib.transforms.Bbox`, optional
            Bbox in inches. Only the given portion of the figure is
            saved. If 'tight', try to figure out the tight bbox of
            the figure. If None, use savefig.bbox

        pad_inches : scalar, optional
            Amount of padding around the figure when bbox_inches is
            'tight'. If None, use savefig.pad_inches

        bbox_extra_artists : list of `~matplotlib.artist.Artist`, optional
            A list of extra artists that will be considered when the
            tight bbox is calculated.

        metadata : dict, optional
            Key/value pairs to store in the image metadata. The supported keys
            and defaults depend on the image format and backend:

            - 'png' with Agg backend: See the parameter ``metadata`` of
              `~.FigureCanvasAgg.print_png`.
            - 'pdf' with pdf backend: See the parameter ``metadata`` of
              `~.backend_pdf.PdfPages`.
            - 'eps' and 'ps' with PS backend: Only 'Creator' is supported.

        pil_kwargs : dict, optional
            Additional keyword arguments that are passed to `PIL.Image.save`
            when saving the figure.  Only applicable for formats that are saved
            using Pillow, i.e. JPEG, TIFF, and (if the keyword is set to a
            non-None value) PNG.
        """

        kwargs.setdefault('dpi', rcParams['savefig.dpi'])
        if "frameon" in kwargs:
            cbook.warn_deprecated("3.1", name="frameon", obj_type="kwarg",
                                  alternative="facecolor")
            frameon = kwargs.pop("frameon")
            if frameon is None:
                frameon = dict.__getitem__(rcParams, 'savefig.frameon')
        else:
            frameon = False  # Won't pass "if frameon:" below.
        if transparent is None:
            transparent = rcParams['savefig.transparent']

        if transparent:
            kwargs.setdefault('facecolor', 'none')
            kwargs.setdefault('edgecolor', 'none')
            original_axes_colors = []
            for ax in self.axes:
                patch = ax.patch
                original_axes_colors.append((patch.get_facecolor(),
                                             patch.get_edgecolor()))
                patch.set_facecolor('none')
                patch.set_edgecolor('none')
        else:
            kwargs.setdefault('facecolor', rcParams['savefig.facecolor'])
            kwargs.setdefault('edgecolor', rcParams['savefig.edgecolor'])

        if frameon:
            original_frameon = self.patch.get_visible()
            self.patch.set_visible(frameon)

        self.canvas.print_figure(fname, **kwargs)

        if frameon:
            self.patch.set_visible(original_frameon)

        if transparent:
            for ax, cc in zip(self.axes, original_axes_colors):
                ax.patch.set_facecolor(cc[0])
                ax.patch.set_edgecolor(cc[1])
