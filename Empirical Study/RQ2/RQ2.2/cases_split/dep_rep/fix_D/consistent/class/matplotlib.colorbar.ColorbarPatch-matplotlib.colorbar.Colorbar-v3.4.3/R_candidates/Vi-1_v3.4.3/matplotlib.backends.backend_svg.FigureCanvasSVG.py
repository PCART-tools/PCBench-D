class FigureCanvasSVG(FigureCanvasBase):
    filetypes = {'svg': 'Scalable Vector Graphics',
                 'svgz': 'Scalable Vector Graphics'}

    fixed_dpi = 72

    def print_svg(self, filename, *args, **kwargs):
        """
        Parameters
        ----------
        filename : str or path-like or file-like
            Output target; if a string, a file will be opened for writing.

        metadata : dict[str, Any], optional
            Metadata in the SVG file defined as key-value pairs of strings,
            datetimes, or lists of strings, e.g., ``{'Creator': 'My software',
            'Contributor': ['Me', 'My Friend'], 'Title': 'Awesome'}``.

            The standard keys and their value types are:

            * *str*: ``'Coverage'``, ``'Description'``, ``'Format'``,
              ``'Identifier'``, ``'Language'``, ``'Relation'``, ``'Source'``,
              ``'Title'``, and ``'Type'``.
            * *str* or *list of str*: ``'Contributor'``, ``'Creator'``,
              ``'Keywords'``, ``'Publisher'``, and ``'Rights'``.
            * *str*, *date*, *datetime*, or *tuple* of same: ``'Date'``. If a
              non-*str*, then it will be formatted as ISO 8601.

            Values have been predefined for ``'Creator'``, ``'Date'``,
            ``'Format'``, and ``'Type'``. They can be removed by setting them
            to `None`.

            Information is encoded as `Dublin Core Metadata`__.

            .. _DC: https://www.dublincore.org/specifications/dublin-core/

            __ DC_
        """
        with cbook.open_file_cm(filename, "w", encoding="utf-8") as fh:

            filename = getattr(fh, 'name', '')
            if not isinstance(filename, str):
                filename = ''

            if cbook.file_requires_unicode(fh):
                detach = False
            else:
                fh = TextIOWrapper(fh, 'utf-8')
                detach = True

            self._print_svg(filename, fh, **kwargs)

            # Detach underlying stream from wrapper so that it remains open in
            # the caller.
            if detach:
                fh.detach()

    def print_svgz(self, filename, *args, **kwargs):
        with cbook.open_file_cm(filename, "wb") as fh, \
                gzip.GzipFile(mode='w', fileobj=fh) as gzipwriter:
            return self.print_svg(gzipwriter)

    @_check_savefig_extra_args
    @_api.delete_parameter("3.4", "dpi")
    def _print_svg(self, filename, fh, *, dpi=None, bbox_inches_restore=None,
                   metadata=None):
        if dpi is None:  # always use this branch after deprecation elapses.
            dpi = self.figure.get_dpi()
        self.figure.set_dpi(72)
        width, height = self.figure.get_size_inches()
        w, h = width * 72, height * 72

        renderer = MixedModeRenderer(
            self.figure, width, height, dpi,
            RendererSVG(w, h, fh, filename, dpi, metadata=metadata),
            bbox_inches_restore=bbox_inches_restore)

        self.figure.draw(renderer)
        renderer.finalize()

    def get_default_filetype(self):
        return 'svg'

    def draw(self):
        _no_output_draw(self.figure)
        return super().draw()
