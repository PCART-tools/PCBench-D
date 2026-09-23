    def print_figure(
            self, filename, dpi=None, facecolor=None, edgecolor=None,
            orientation='portrait', format=None, *,
            bbox_inches=None, pad_inches=None, bbox_extra_artists=None,
            backend=None, **kwargs):
        """
        Render the figure to hardcopy. Set the figure patch face and edge
        colors.  This is useful because some of the GUIs have a gray figure
        face color background and you'll probably want to override this on
        hardcopy.

        Parameters
        ----------
        filename : str or path-like or file-like
            The file where the figure is saved.

        dpi : float, default: :rc:`savefig.dpi`
            The dots per inch to save the figure in.

        facecolor : color or 'auto', default: :rc:`savefig.facecolor`
            The facecolor of the figure.  If 'auto', use the current figure
            facecolor.

        edgecolor : color or 'auto', default: :rc:`savefig.edgecolor`
            The edgecolor of the figure.  If 'auto', use the current figure
            edgecolor.

        orientation : {'landscape', 'portrait'}, default: 'portrait'
            Only currently applies to PostScript printing.

        format : str, optional
            Force a specific file format. If not given, the format is inferred
            from the *filename* extension, and if that fails from
            :rc:`savefig.format`.

        bbox_inches : 'tight' or `.Bbox`, default: :rc:`savefig.bbox`
            Bounding box in inches: only the given portion of the figure is
            saved.  If 'tight', try to figure out the tight bbox of the figure.

        pad_inches : float, default: :rc:`savefig.pad_inches`
            Amount of padding around the figure when *bbox_inches* is 'tight'.

        bbox_extra_artists : list of `~matplotlib.artist.Artist`, optional
            A list of extra artists that will be considered when the
            tight bbox is calculated.

        backend : str, optional
            Use a non-default backend to render the file, e.g. to render a
            png file with the "cairo" backend rather than the default "agg",
            or a pdf file with the "pgf" backend rather than the default
            "pdf".  Note that the default backend is normally sufficient.  See
            :ref:`the-builtin-backends` for a list of valid backends for each
            file format.  Custom backends can be referenced as "module://...".
        """
        if format is None:
            # get format from filename, or from backend's default filetype
            if isinstance(filename, os.PathLike):
                filename = os.fspath(filename)
            if isinstance(filename, str):
                format = os.path.splitext(filename)[1][1:]
            if format is None or format == '':
                format = self.get_default_filetype()
                if isinstance(filename, str):
                    filename = filename.rstrip('.') + '.' + format
        format = format.lower()

        # get canvas object and print method for format
        canvas = self._get_output_canvas(backend, format)
        print_method = getattr(canvas, 'print_%s' % format)

        if dpi is None:
            dpi = rcParams['savefig.dpi']
        if dpi == 'figure':
            dpi = getattr(self.figure, '_original_dpi', self.figure.dpi)

        # Remove the figure manager, if any, to avoid resizing the GUI widget.
        with cbook._setattr_cm(self, manager=None), \
             cbook._setattr_cm(self.figure, dpi=dpi), \
             cbook._setattr_cm(canvas, _device_pixel_ratio=1), \
             cbook._setattr_cm(canvas, _is_saving=True), \
             ExitStack() as stack:

            for prop in ["facecolor", "edgecolor"]:
                color = locals()[prop]
                if color is None:
                    color = rcParams[f"savefig.{prop}"]
                if not cbook._str_equal(color, "auto"):
                    stack.enter_context(self.figure._cm_set(**{prop: color}))

            if bbox_inches is None:
                bbox_inches = rcParams['savefig.bbox']

            if (self.figure.get_constrained_layout() or
                    bbox_inches == "tight"):
                # we need to trigger a draw before printing to make sure
                # CL works.  "tight" also needs a draw to get the right
                # locations:
                renderer = _get_renderer(
                    self.figure,
                    functools.partial(
                        print_method, orientation=orientation)
                )
                with getattr(renderer, "_draw_disabled", nullcontext)():
                    self.figure.draw(renderer)

            if bbox_inches:
                if bbox_inches == "tight":
                    bbox_inches = self.figure.get_tightbbox(
                        renderer, bbox_extra_artists=bbox_extra_artists)
                    if pad_inches is None:
                        pad_inches = rcParams['savefig.pad_inches']
                    bbox_inches = bbox_inches.padded(pad_inches)

                # call adjust_bbox to save only the given area
                restore_bbox = tight_bbox.adjust_bbox(self.figure, bbox_inches,
                                                      canvas.fixed_dpi)

                _bbox_inches_restore = (bbox_inches, restore_bbox)
            else:
                _bbox_inches_restore = None

            # we have already done CL above, so turn it off:
            stack.enter_context(self.figure._cm_set(constrained_layout=False))
            try:
                # _get_renderer may change the figure dpi (as vector formats
                # force the figure dpi to 72), so we need to set it again here.
                with cbook._setattr_cm(self.figure, dpi=dpi):
                    result = print_method(
                        filename,
                        facecolor=facecolor,
                        edgecolor=edgecolor,
                        orientation=orientation,
                        bbox_inches_restore=_bbox_inches_restore,
                        **kwargs)
            finally:
                if bbox_inches and restore_bbox:
                    restore_bbox()

                self.figure.set_canvas(self)
            return result
