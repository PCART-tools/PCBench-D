    def savefig(self, fname, *, transparent=None, **kwargs):
        """
        Save the current figure.

        Call signature::

          savefig(fname, *, dpi='figure', format=None, metadata=None,
                  bbox_inches=None, pad_inches=0.1,
                  facecolor='auto', edgecolor='auto',
                  backend=None, **kwargs
                 )

        The available output formats depend on the backend being used.

        Parameters
        ----------
        fname : str or path-like or binary file-like
            A path, or a Python file-like object, or
            possibly some backend-dependent object such as
            `matplotlib.backends.backend_pdf.PdfPages`.

            If *format* is set, it determines the output format, and the file
            is saved as *fname*.  Note that *fname* is used verbatim, and there
            is no attempt to make the extension, if any, of *fname* match
            *format*, and no extension is appended.

            If *format* is not set, then the format is inferred from the
            extension of *fname*, if there is one.  If *format* is not
            set and *fname* has no extension, then the file is saved with
            :rc:`savefig.format` and the appropriate extension is appended to
            *fname*.

        Other Parameters
        ----------------
        dpi : float or 'figure', default: :rc:`savefig.dpi`
            The resolution in dots per inch.  If 'figure', use the figure's
            dpi value.

        format : str
            The file format, e.g. 'png', 'pdf', 'svg', ... The behavior when
            this is unset is documented under *fname*.

        metadata : dict, optional
            Key/value pairs to store in the image metadata. The supported keys
            and defaults depend on the image format and backend:

            - 'png' with Agg backend: See the parameter ``metadata`` of
              `~.FigureCanvasAgg.print_png`.
            - 'pdf' with pdf backend: See the parameter ``metadata`` of
              `~.backend_pdf.PdfPages`.
            - 'svg' with svg backend: See the parameter ``metadata`` of
              `~.FigureCanvasSVG.print_svg`.
            - 'eps' and 'ps' with PS backend: Only 'Creator' is supported.

            Not supported for 'pgf', 'raw', and 'rgba' as those formats do not support
            embedding metadata.
            Does not currently support 'jpg', 'tiff', or 'webp', but may include
            embedding EXIF metadata in the future.

        bbox_inches : str or `.Bbox`, default: :rc:`savefig.bbox`
            Bounding box in inches: only the given portion of the figure is
            saved.  If 'tight', try to figure out the tight bbox of the figure.

        pad_inches : float or 'layout', default: :rc:`savefig.pad_inches`
            Amount of padding in inches around the figure when bbox_inches is
            'tight'. If 'layout' use the padding from the constrained or
            compressed layout engine; ignored if one of those engines is not in
            use.

        facecolor : color or 'auto', default: :rc:`savefig.facecolor`
            The facecolor of the figure.  If 'auto', use the current figure
            facecolor.

        edgecolor : color or 'auto', default: :rc:`savefig.edgecolor`
            The edgecolor of the figure.  If 'auto', use the current figure
            edgecolor.

        backend : str, optional
            Use a non-default backend to render the file, e.g. to render a
            png file with the "cairo" backend rather than the default "agg",
            or a pdf file with the "pgf" backend rather than the default
            "pdf".  Note that the default backend is normally sufficient.  See
            :ref:`the-builtin-backends` for a list of valid backends for each
            file format.  Custom backends can be referenced as "module://...".

        orientation : {'landscape', 'portrait'}
            Currently only supported by the postscript backend.

        papertype : str
            One of 'letter', 'legal', 'executive', 'ledger', 'a0' through
            'a10', 'b0' through 'b10'. Only supported for postscript
            output.

        transparent : bool
            If *True*, the Axes patches will all be transparent; the
            Figure patch will also be transparent unless *facecolor*
            and/or *edgecolor* are specified via kwargs.

            If *False* has no effect and the color of the Axes and
            Figure patches are unchanged (unless the Figure patch
            is specified via the *facecolor* and/or *edgecolor* keyword
            arguments in which case those colors are used).

            The transparency of these patches will be restored to their
            original values upon exit of this function.

            This is useful, for example, for displaying
            a plot on top of a colored background on a web page.

        bbox_extra_artists : list of `~matplotlib.artist.Artist`, optional
            A list of extra artists that will be considered when the
            tight bbox is calculated.

        pil_kwargs : dict, optional
            Additional keyword arguments that are passed to
            `PIL.Image.Image.save` when saving the figure.

        """

        kwargs.setdefault('dpi', mpl.rcParams['savefig.dpi'])
        if transparent is None:
            transparent = mpl.rcParams['savefig.transparent']

        with ExitStack() as stack:
            if transparent:
                def _recursively_make_subfig_transparent(exit_stack, subfig):
                    exit_stack.enter_context(
                        subfig.patch._cm_set(
                            facecolor="none", edgecolor="none"))
                    for ax in subfig.axes:
                        exit_stack.enter_context(
                            ax.patch._cm_set(
                                facecolor="none", edgecolor="none"))
                    for sub_subfig in subfig.subfigs:
                        _recursively_make_subfig_transparent(
                            exit_stack, sub_subfig)

                def _recursively_make_axes_transparent(exit_stack, ax):
                    exit_stack.enter_context(
                        ax.patch._cm_set(facecolor="none", edgecolor="none"))
                    for child_ax in ax.child_axes:
                        exit_stack.enter_context(
                            child_ax.patch._cm_set(
                                facecolor="none", edgecolor="none"))
                    for child_childax in ax.child_axes:
                        _recursively_make_axes_transparent(
                            exit_stack, child_childax)

                kwargs.setdefault('facecolor', 'none')
                kwargs.setdefault('edgecolor', 'none')
                # set subfigure to appear transparent in printed image
                for subfig in self.subfigs:
                    _recursively_make_subfig_transparent(stack, subfig)
                # set axes to be transparent
                for ax in self.axes:
                    _recursively_make_axes_transparent(stack, ax)
            self.canvas.print_figure(fname, **kwargs)
