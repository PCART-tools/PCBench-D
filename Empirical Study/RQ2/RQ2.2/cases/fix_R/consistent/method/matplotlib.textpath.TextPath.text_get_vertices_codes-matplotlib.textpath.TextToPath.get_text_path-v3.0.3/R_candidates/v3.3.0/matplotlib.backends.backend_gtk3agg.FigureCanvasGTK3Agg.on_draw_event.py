    def on_draw_event(self, widget, ctx):
        """GtkDrawable draw event, like expose_event in GTK 2.X."""
        allocation = self.get_allocation()
        w, h = allocation.width, allocation.height

        if not len(self._bbox_queue):
            Gtk.render_background(
                self.get_style_context(), ctx,
                allocation.x, allocation.y,
                allocation.width, allocation.height)
            bbox_queue = [transforms.Bbox([[0, 0], [w, h]])]
        else:
            bbox_queue = self._bbox_queue

        ctx = backend_cairo._to_context(ctx)

        for bbox in bbox_queue:
            x = int(bbox.x0)
            y = h - int(bbox.y1)
            width = int(bbox.x1) - int(bbox.x0)
            height = int(bbox.y1) - int(bbox.y0)

            buf = cbook._unmultiplied_rgba8888_to_premultiplied_argb32(
                np.asarray(self.copy_from_bbox(bbox)))
            image = cairo.ImageSurface.create_for_data(
                buf.ravel().data, cairo.FORMAT_ARGB32, width, height)
            ctx.set_source_surface(image, x, y)
            ctx.paint()

        if len(self._bbox_queue):
            self._bbox_queue = []

        return False
