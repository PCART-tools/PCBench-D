    def _print_image(self, filename, format, *args, **kwargs):
        if self.flags() & gtk.REALIZED == 0:
            # for self.window(for pixmap) and has a side effect of altering
            # figure width,height (via configure-event?)
            gtk.DrawingArea.realize(self)

        width, height = self.get_width_height()
        pixmap = gdk.Pixmap (self.window, width, height)
        self._renderer.set_pixmap (pixmap)
        self._render_figure(pixmap, width, height)

        # jpg colors don't match the display very well, png colors match
        # better
        pixbuf = gdk.Pixbuf(gdk.COLORSPACE_RGB, 0, 8, width, height)
        pixbuf.get_from_drawable(pixmap, pixmap.get_colormap(),
                                     0, 0, 0, 0, width, height)

        # set the default quality, if we are writing a JPEG.
        # http://www.pygtk.org/docs/pygtk/class-gdkpixbuf.html#method-gdkpixbuf--save
        options = {k: kwargs[k] for k in ['quality'] if k in kwargs}
        if format in ['jpg', 'jpeg']:
            options.setdefault('quality', rcParams['savefig.jpeg_quality'])
            options['quality'] = str(options['quality'])

        if isinstance(filename, six.string_types):
            try:
                pixbuf.save(filename, format, options=options)
            except gobject.GError as exc:
                error_msg_gtk('Save figure failure:\n%s' % (exc,), parent=self)
        elif is_writable_file_like(filename):
            if hasattr(pixbuf, 'save_to_callback'):
                def save_callback(buf, data=None):
                    data.write(buf)
                try:
                    pixbuf.save_to_callback(save_callback, format, user_data=filename, options=options)
                except gobject.GError as exc:
                    error_msg_gtk('Save figure failure:\n%s' % (exc,), parent=self)
            else:
                raise ValueError("Saving to a Python file-like object is only supported by PyGTK >= 2.8")
        else:
            raise ValueError("filename must be a path or a file-like object")
