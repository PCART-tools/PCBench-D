    def print_figure(self, filename, dpi=None, facecolor=None, edgecolor=None,
                     orientation='portrait', format=None,
                     *, bbox_inches=None, **kwargs):
        """
        Render the figure to hardcopy. Set the figure patch face and edge
        colors.  This is useful because some of the GUIs have a gray figure
        face color background and you'll probably want to override this on
        hardcopy.

        Parameters
        ----------
        filename
            can also be a file object on image backends

        orientation : {'landscape', 'portrait'}, default: 'portrait'
            only currently applies to PostScript printing.

        dpi : scalar, optional
            the dots per inch to save the figure in; if None, use savefig.dpi

        facecolor : color, default: :rc:`savefig.facecolor`
            The facecolor of the figure.

        edgecolor : color, default: :rc:`savefig.edgecolor`
            The edgecolor of the figure.

        format : str, optional
            Force a specific file format. If not given, the format is inferred
            from the *filename* extension, and if that fails from
            :rc:`savefig.format`.

        bbox_inches : 'tight' or `~matplotlib.transforms.Bbox`, \
default: :rc:`savefig.bbox`
            Bbox in inches. Only the given portion of the figure is
            saved. If 'tight', try to figure out the tight bbox of
            the figure.

        pad_inches : float, default: :rc:`savefig.pad_inches`
            Amount of padding around the figure when *bbox_inches* is 'tight'.

        bbox_extra_artists : list of `~matplotlib.artist.Artist`, optional
            A list of extra artists that will be considered when the
            tight bbox is calculated.

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
        canvas = self._get_output_canvas(format)
        print_method = getattr(canvas, 'print_%s' % format)

        if dpi is None:
            dpi = rcParams['savefig.dpi']
        if dpi == 'figure':
            dpi = getattr(self.figure, '_original_dpi', self.figure.dpi)

        # Remove the figure manager, if any, to avoid resizing the GUI widget.
        # Some code (e.g. Figure.show) differentiates between having *no*
        # manager and a *None* manager, which should be fixed at some point,
        # but this should be fine.
        with cbook._setattr_cm(self, _is_saving=True, manager=None), \
                cbook._setattr_cm(self.figure, dpi=dpi):

            if facecolor is None:
                facecolor = rcParams['savefig.facecolor']
            if edgecolor is None:
                edgecolor = rcParams['savefig.edgecolor']

            origfacecolor = self.figure.get_facecolor()
            origedgecolor = self.figure.get_edgecolor()

            self.figure.set_facecolor(facecolor)
            self.figure.set_edgecolor(edgecolor)

            if bbox_inches is None:
                bbox_inches = rcParams['savefig.bbox']

            if bbox_inches:
                if bbox_inches == "tight":
                    renderer = _get_renderer(
                        self.figure,
                        functools.partial(
                            print_method, dpi=dpi, orientation=orientation))
                    self.figure.draw(renderer)
                    bbox_artists = kwargs.pop("bbox_extra_artists", None)
                    bbox_inches = self.figure.get_tightbbox(renderer,
                            bbox_extra_artists=bbox_artists)
                    pad = kwargs.pop("pad_inches", None)
                    if pad is None:
                        pad = rcParams['savefig.pad_inches']

                    bbox_inches = bbox_inches.padded(pad)

                # call adjust_bbox to save only the given area
                restore_bbox = tight_bbox.adjust_bbox(self.figure, bbox_inches,
                                                      canvas.fixed_dpi)

                _bbox_inches_restore = (bbox_inches, restore_bbox)
            else:
                _bbox_inches_restore = None

            try:
                result = print_method(
                    filename,
                    dpi=dpi,
                    facecolor=facecolor,
                    edgecolor=edgecolor,
                    orientation=orientation,
                    bbox_inches_restore=_bbox_inches_restore,
                    **kwargs)
            finally:
                if bbox_inches and restore_bbox:
                    restore_bbox()

                self.figure.set_facecolor(origfacecolor)
                self.figure.set_edgecolor(origedgecolor)
                self.figure.set_canvas(self)
            return result
