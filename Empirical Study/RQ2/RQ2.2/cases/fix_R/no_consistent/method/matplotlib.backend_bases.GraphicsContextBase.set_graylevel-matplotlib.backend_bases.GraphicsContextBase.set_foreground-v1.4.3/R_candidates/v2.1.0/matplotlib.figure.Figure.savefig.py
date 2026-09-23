    def savefig(self, fname, **kwargs):
        """
        Save the current figure.

        Call signature::

          savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                  orientation='portrait', papertype=None, format=None,
                  transparent=False, bbox_inches=None, pad_inches=0.1,
                  frameon=None)

        The output formats available depend on the backend being used.

        Arguments:

          *fname*:
            A string containing a path to a filename, or a Python
            file-like object, or possibly some backend-dependent object
            such as :class:`~matplotlib.backends.backend_pdf.PdfPages`.

            If *format* is *None* and *fname* is a string, the output
            format is deduced from the extension of the filename. If
            the filename has no extension, the value of the rc parameter
            ``savefig.format`` is used.

            If *fname* is not a string, remember to specify *format* to
            ensure that the correct backend is used.

        Keyword arguments:

          *dpi*: [ *None* | ``scalar > 0`` | 'figure']
            The resolution in dots per inch.  If *None* it will default to
            the value ``savefig.dpi`` in the matplotlibrc file. If 'figure'
            it will set the dpi to be the value of the figure.

          *facecolor*, *edgecolor*:
            the colors of the figure rectangle

          *orientation*: [ 'landscape' | 'portrait' ]
            not supported on all backends; currently only on postscript output

          *papertype*:
            One of 'letter', 'legal', 'executive', 'ledger', 'a0' through
            'a10', 'b0' through 'b10'. Only supported for postscript
            output.

          *format*:
            One of the file extensions supported by the active
            backend.  Most backends support png, pdf, ps, eps and svg.

          *transparent*:
            If *True*, the axes patches will all be transparent; the
            figure patch will also be transparent unless facecolor
            and/or edgecolor are specified via kwargs.
            This is useful, for example, for displaying
            a plot on top of a colored background on a web page.  The
            transparency of these patches will be restored to their
            original values upon exit of this function.

          *frameon*:
            If *True*, the figure patch will be colored, if *False*, the
            figure background will be transparent.  If not provided, the
            rcParam 'savefig.frameon' will be used.

          *bbox_inches*:
            Bbox in inches. Only the given portion of the figure is
            saved. If 'tight', try to figure out the tight bbox of
            the figure.

          *pad_inches*:
            Amount of padding around the figure when bbox_inches is
            'tight'.

          *bbox_extra_artists*:
            A list of extra artists that will be considered when the
            tight bbox is calculated.

        """
        kwargs.setdefault('dpi', rcParams['savefig.dpi'])
        frameon = kwargs.pop('frameon', rcParams['savefig.frameon'])
        transparent = kwargs.pop('transparent',
                                 rcParams['savefig.transparent'])

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
            original_frameon = self.get_frameon()
            self.set_frameon(frameon)

        self.canvas.print_figure(fname, **kwargs)

        if frameon:
            self.set_frameon(original_frameon)

        if transparent:
            for ax, cc in zip(self.axes, original_axes_colors):
                ax.patch.set_facecolor(cc[0])
                ax.patch.set_edgecolor(cc[1])
