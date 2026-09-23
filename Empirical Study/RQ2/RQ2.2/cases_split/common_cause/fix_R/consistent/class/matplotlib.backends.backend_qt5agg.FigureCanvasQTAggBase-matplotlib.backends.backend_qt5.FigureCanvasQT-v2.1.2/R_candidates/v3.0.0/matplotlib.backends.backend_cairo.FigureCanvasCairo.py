class FigureCanvasCairo(FigureCanvasBase):
    supports_blit = False

    def print_png(self, fobj, *args, **kwargs):
        self._get_printed_image_surface().write_to_png(fobj)

    def print_rgba(self, fobj, *args, **kwargs):
        width, height = self.get_width_height()
        buf = self._get_printed_image_surface().get_data()
        fobj.write(cbook._premultiplied_argb32_to_unmultiplied_rgba8888(
            np.asarray(buf).reshape((width, height, 4))))

    print_raw = print_rgba

    def _get_printed_image_surface(self):
        width, height = self.get_width_height()
        renderer = RendererCairo(self.figure.dpi)
        renderer.set_width_height(width, height)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        renderer.set_ctx_from_surface(surface)
        self.figure.draw(renderer)
        return surface

    def print_pdf(self, fobj, *args, **kwargs):
        return self._save(fobj, 'pdf', *args, **kwargs)

    def print_ps(self, fobj, *args, **kwargs):
        return self._save(fobj, 'ps', *args, **kwargs)

    def print_svg(self, fobj, *args, **kwargs):
        return self._save(fobj, 'svg', *args, **kwargs)

    def print_svgz(self, fobj, *args, **kwargs):
        return self._save(fobj, 'svgz', *args, **kwargs)

    def _save(self, fo, fmt, **kwargs):
        # save PDF/PS/SVG
        orientation = kwargs.get('orientation', 'portrait')

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
            surface = cairo.PSSurface(fo, width_in_points, height_in_points)
        elif fmt == 'pdf':
            if not hasattr(cairo, 'PDFSurface'):
                raise RuntimeError('cairo has not been compiled with PDF '
                                   'support enabled')
            surface = cairo.PDFSurface(fo, width_in_points, height_in_points)
        elif fmt in ('svg', 'svgz'):
            if not hasattr(cairo, 'SVGSurface'):
                raise RuntimeError('cairo has not been compiled with SVG '
                                   'support enabled')
            if fmt == 'svgz':
                if isinstance(fo, str):
                    fo = gzip.GzipFile(fo, 'wb')
                else:
                    fo = gzip.GzipFile(None, 'wb', fileobj=fo)
            surface = cairo.SVGSurface(fo, width_in_points, height_in_points)
        else:
            warnings.warn("unknown format: %s" % fmt, stacklevel=2)
            return

        # surface.set_dpi() can be used
        renderer = RendererCairo(self.figure.dpi)
        renderer.set_width_height(width_in_points, height_in_points)
        renderer.set_ctx_from_surface(surface)
        ctx = renderer.gc.ctx

        if orientation == 'landscape':
            ctx.rotate(np.pi / 2)
            ctx.translate(0, -height_in_points)
            # Perhaps add an '%%Orientation: Landscape' comment?

        self.figure.draw(renderer)

        ctx.show_page()
        surface.finish()
        if fmt == 'svgz':
            fo.close()
