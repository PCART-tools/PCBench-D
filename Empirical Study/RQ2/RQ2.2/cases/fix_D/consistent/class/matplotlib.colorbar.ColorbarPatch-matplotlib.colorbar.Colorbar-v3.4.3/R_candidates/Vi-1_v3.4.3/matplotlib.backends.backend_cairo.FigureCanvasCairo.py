class FigureCanvasCairo(FigureCanvasBase):

    def copy_from_bbox(self, bbox):
        surface = self._renderer.gc.ctx.get_target()
        if not isinstance(surface, cairo.ImageSurface):
            raise RuntimeError(
                "copy_from_bbox only works when rendering to an ImageSurface")
        sw = surface.get_width()
        sh = surface.get_height()
        x0 = math.ceil(bbox.x0)
        x1 = math.floor(bbox.x1)
        y0 = math.ceil(sh - bbox.y1)
        y1 = math.floor(sh - bbox.y0)
        if not (0 <= x0 and x1 <= sw and bbox.x0 <= bbox.x1
                and 0 <= y0 and y1 <= sh and bbox.y0 <= bbox.y1):
            raise ValueError("Invalid bbox")
        sls = slice(y0, y0 + max(y1 - y0, 0)), slice(x0, x0 + max(x1 - x0, 0))
        data = (np.frombuffer(surface.get_data(), np.uint32)
                .reshape((sh, sw))[sls].copy())
        return _CairoRegion(sls, data)

    def restore_region(self, region):
        surface = self._renderer.gc.ctx.get_target()
        if not isinstance(surface, cairo.ImageSurface):
            raise RuntimeError(
                "restore_region only works when rendering to an ImageSurface")
        surface.flush()
        sw = surface.get_width()
        sh = surface.get_height()
        sly, slx = region._slices
        (np.frombuffer(surface.get_data(), np.uint32)
         .reshape((sh, sw))[sly, slx]) = region._data
        surface.mark_dirty_rectangle(
            slx.start, sly.start, slx.stop - slx.start, sly.stop - sly.start)

    @_check_savefig_extra_args
    def print_png(self, fobj):
        self._get_printed_image_surface().write_to_png(fobj)

    @_check_savefig_extra_args
    def print_rgba(self, fobj):
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

    @_check_savefig_extra_args
    def _save(self, fo, fmt, *, orientation='portrait'):
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
            raise ValueError("Unknown format: {!r}".format(fmt))

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
