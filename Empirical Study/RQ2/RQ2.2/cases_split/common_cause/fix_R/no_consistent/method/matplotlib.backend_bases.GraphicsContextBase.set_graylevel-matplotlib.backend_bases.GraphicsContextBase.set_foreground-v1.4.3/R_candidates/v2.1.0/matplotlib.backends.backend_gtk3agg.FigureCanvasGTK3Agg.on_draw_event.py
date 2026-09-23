    def on_draw_event(self, widget, ctx):
        """ GtkDrawable draw event, like expose_event in GTK 2.X
        """
        allocation = self.get_allocation()
        w, h = allocation.width, allocation.height

        if not len(self._bbox_queue):
            self._render_figure(w, h)
            bbox_queue = [transforms.Bbox([[0, 0], [w, h]])]
        else:
            bbox_queue = self._bbox_queue

        if HAS_CAIRO_CFFI:
            ctx = cairo.Context._from_pointer(
                cairo.ffi.cast('cairo_t **',
                               id(ctx) + object.__basicsize__)[0],
                incref=True)

        for bbox in bbox_queue:
            area = self.copy_from_bbox(bbox)
            buf = np.fromstring(area.to_string_argb(), dtype='uint8')

            x = int(bbox.x0)
            y = h - int(bbox.y1)
            width = int(bbox.x1) - int(bbox.x0)
            height = int(bbox.y1) - int(bbox.y0)

            if HAS_CAIRO_CFFI:
                image = cairo.ImageSurface.create_for_data(
                    buf.data, cairo.FORMAT_ARGB32, width, height)
            else:
                image = cairo.ImageSurface.create_for_data(
                    buf, cairo.FORMAT_ARGB32, width, height)
            ctx.set_source_surface(image, x, y)
            ctx.paint()

        if len(self._bbox_queue):
            self._bbox_queue = []

        return False
