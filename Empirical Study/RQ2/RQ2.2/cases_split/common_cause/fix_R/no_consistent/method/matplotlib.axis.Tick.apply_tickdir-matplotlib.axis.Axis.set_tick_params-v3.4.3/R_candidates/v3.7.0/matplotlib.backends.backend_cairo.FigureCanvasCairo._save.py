    def _save(self, fmt, fobj, *, orientation='portrait'):
        # save PDF/PS/SVG

        dpi = 72
        self.figure.dpi = dpi
        w_in, h_in = self.figure.get_size_inches()
        width_in_points, height_in_points = w_in * dpi, h_in * dpi

        if orientation == 'landscape':
            width_in_points, height_in_points = (
                height_in_points, width_in_points)

        if fmt == 'ps':
            if not hasattr(cairo, 'PSSurface'):
                raise RuntimeError('cairo has not been compiled with PS '
                                   'support enabled')
            surface = cairo.PSSurface(fobj, width_in_points, height_in_points)
        elif fmt == 'pdf':
            if not hasattr(cairo, 'PDFSurface'):
                raise RuntimeError('cairo has not been compiled with PDF '
                                   'support enabled')
            surface = cairo.PDFSurface(fobj, width_in_points, height_in_points)
        elif fmt in ('svg', 'svgz'):
            if not hasattr(cairo, 'SVGSurface'):
                raise RuntimeError('cairo has not been compiled with SVG '
                                   'support enabled')
            if fmt == 'svgz':
                if isinstance(fobj, str):
                    fobj = gzip.GzipFile(fobj, 'wb')
                else:
                    fobj = gzip.GzipFile(None, 'wb', fileobj=fobj)
            surface = cairo.SVGSurface(fobj, width_in_points, height_in_points)
        else:
            raise ValueError("Unknown format: {!r}".format(fmt))

        self._renderer.dpi = self.figure.dpi
        self._renderer.set_context(cairo.Context(surface))
        ctx = self._renderer.gc.ctx

        if orientation == 'landscape':
            ctx.rotate(np.pi / 2)
            ctx.translate(0, -height_in_points)
            # Perhaps add an '%%Orientation: Landscape' comment?

        self.figure.draw(self._renderer)

        ctx.show_page()
        surface.finish()
        if fmt == 'svgz':
            fobj.close()
