class FigureCanvasGTK3(FigureCanvasBase, Gtk.DrawingArea):
    required_interactive_framework = "gtk3"
    _timer_cls = TimerGTK3
    manager_class = _api.classproperty(lambda cls: FigureManagerGTK3)
    # Setting this as a static constant prevents
    # this resulting expression from leaking
    event_mask = (Gdk.EventMask.BUTTON_PRESS_MASK
                  | Gdk.EventMask.BUTTON_RELEASE_MASK
                  | Gdk.EventMask.EXPOSURE_MASK
                  | Gdk.EventMask.KEY_PRESS_MASK
                  | Gdk.EventMask.KEY_RELEASE_MASK
                  | Gdk.EventMask.ENTER_NOTIFY_MASK
                  | Gdk.EventMask.LEAVE_NOTIFY_MASK
                  | Gdk.EventMask.POINTER_MOTION_MASK
                  | Gdk.EventMask.SCROLL_MASK)

    def __init__(self, figure=None):
        super().__init__(figure=figure)

        self._idle_draw_id = 0
        self._rubberband_rect = None

        self.connect('scroll_event',         self.scroll_event)
        self.connect('button_press_event',   self.button_press_event)
        self.connect('button_release_event', self.button_release_event)
        self.connect('configure_event',      self.configure_event)
        self.connect('screen-changed',       self._update_device_pixel_ratio)
        self.connect('notify::scale-factor', self._update_device_pixel_ratio)
        self.connect('draw',                 self.on_draw_event)
        self.connect('draw',                 self._post_draw)
        self.connect('key_press_event',      self.key_press_event)
        self.connect('key_release_event',    self.key_release_event)
        self.connect('motion_notify_event',  self.motion_notify_event)
        self.connect('enter_notify_event',   self.enter_notify_event)
        self.connect('leave_notify_event',   self.leave_notify_event)
        self.connect('size_allocate',        self.size_allocate)

        self.set_events(self.__class__.event_mask)

        self.set_can_focus(True)

        css = Gtk.CssProvider()
        css.load_from_data(b".matplotlib-canvas { background-color: white; }")
        style_ctx = self.get_style_context()
        style_ctx.add_provider(css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        style_ctx.add_class("matplotlib-canvas")

    def destroy(self):
        CloseEvent("close_event", self)._process()

    def set_cursor(self, cursor):
        # docstring inherited
        window = self.get_property("window")
        if window is not None:
            window.set_cursor(_mpl_to_gtk_cursor(cursor))
            context = GLib.MainContext.default()
            context.iteration(True)

    def _mpl_coords(self, event=None):
        """
        Convert the position of a GTK event, or of the current cursor position
        if *event* is None, to Matplotlib coordinates.

        GTK use logical pixels, but the figure is scaled to physical pixels for
        rendering.  Transform to physical pixels so that all of the down-stream
        transforms work as expected.

        Also, the origin is different and needs to be corrected.
        """
        if event is None:
            window = self.get_window()
            t, x, y, state = window.get_device_position(
                window.get_display().get_device_manager().get_client_pointer())
        else:
            x, y = event.x, event.y
        x = x * self.device_pixel_ratio
        # flip y so y=0 is bottom of canvas
        y = self.figure.bbox.height - y * self.device_pixel_ratio
        return x, y

    def scroll_event(self, widget, event):
        step = 1 if event.direction == Gdk.ScrollDirection.UP else -1
        MouseEvent("scroll_event", self, *self._mpl_coords(event), step=step,
                   guiEvent=event)._process()
        return False  # finish event propagation?

    def button_press_event(self, widget, event):
        MouseEvent("button_press_event", self,
                   *self._mpl_coords(event), event.button,
                   guiEvent=event)._process()
        return False  # finish event propagation?

    def button_release_event(self, widget, event):
        MouseEvent("button_release_event", self,
                   *self._mpl_coords(event), event.button,
                   guiEvent=event)._process()
        return False  # finish event propagation?

    def key_press_event(self, widget, event):
        KeyEvent("key_press_event", self,
                 self._get_key(event), *self._mpl_coords(),
                 guiEvent=event)._process()
        return True  # stop event propagation

    def key_release_event(self, widget, event):
        KeyEvent("key_release_event", self,
                 self._get_key(event), *self._mpl_coords(),
                 guiEvent=event)._process()
        return True  # stop event propagation

    def motion_notify_event(self, widget, event):
        MouseEvent("motion_notify_event", self, *self._mpl_coords(event),
                   guiEvent=event)._process()
        return False  # finish event propagation?

    def enter_notify_event(self, widget, event):
        LocationEvent("figure_enter_event", self, *self._mpl_coords(event),
                      guiEvent=event)._process()

    def leave_notify_event(self, widget, event):
        LocationEvent("figure_leave_event", self, *self._mpl_coords(event),
                      guiEvent=event)._process()

    def size_allocate(self, widget, allocation):
        dpival = self.figure.dpi
        winch = allocation.width * self.device_pixel_ratio / dpival
        hinch = allocation.height * self.device_pixel_ratio / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)
        ResizeEvent("resize_event", self)._process()
        self.draw_idle()

    def _get_key(self, event):
        unikey = chr(Gdk.keyval_to_unicode(event.keyval))
        key = cbook._unikey_or_keysym_to_mplkey(
            unikey,
            Gdk.keyval_name(event.keyval))
        modifiers = [
            (Gdk.ModifierType.CONTROL_MASK, 'ctrl'),
            (Gdk.ModifierType.MOD1_MASK, 'alt'),
            (Gdk.ModifierType.SHIFT_MASK, 'shift'),
            (Gdk.ModifierType.MOD4_MASK, 'super'),
        ]
        for key_mask, prefix in modifiers:
            if event.state & key_mask:
                if not (prefix == 'shift' and unikey.isprintable()):
                    key = f'{prefix}+{key}'
        return key

    def _update_device_pixel_ratio(self, *args, **kwargs):
        # We need to be careful in cases with mixed resolution displays if
        # device_pixel_ratio changes.
        if self._set_device_pixel_ratio(self.get_scale_factor()):
            # The easiest way to resize the canvas is to emit a resize event
            # since we implement all the logic for resizing the canvas for that
            # event.
            self.queue_resize()
            self.queue_draw()

    def configure_event(self, widget, event):
        if widget.get_property("window") is None:
            return
        w = event.width * self.device_pixel_ratio
        h = event.height * self.device_pixel_ratio
        if w < 3 or h < 3:
            return  # empty fig
        # resize the figure (in inches)
        dpi = self.figure.dpi
        self.figure.set_size_inches(w / dpi, h / dpi, forward=False)
        return False  # finish event propagation?

    def _draw_rubberband(self, rect):
        self._rubberband_rect = rect
        # TODO: Only update the rubberband area.
        self.queue_draw()

    def _post_draw(self, widget, ctx):
        if self._rubberband_rect is None:
            return

        x0, y0, w, h = (dim / self.device_pixel_ratio
                        for dim in self._rubberband_rect)
        x1 = x0 + w
        y1 = y0 + h

        # Draw the lines from x0, y0 towards x1, y1 so that the
        # dashes don't "jump" when moving the zoom box.
        ctx.move_to(x0, y0)
        ctx.line_to(x0, y1)
        ctx.move_to(x0, y0)
        ctx.line_to(x1, y0)
        ctx.move_to(x0, y1)
        ctx.line_to(x1, y1)
        ctx.move_to(x1, y0)
        ctx.line_to(x1, y1)

        ctx.set_antialias(1)
        ctx.set_line_width(1)
        ctx.set_dash((3, 3), 0)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke_preserve()

        ctx.set_dash((3, 3), 3)
        ctx.set_source_rgb(1, 1, 1)
        ctx.stroke()

    def on_draw_event(self, widget, ctx):
        # to be overwritten by GTK3Agg or GTK3Cairo
        pass

    def draw(self):
        # docstring inherited
        if self.is_drawable():
            self.queue_draw()

    def draw_idle(self):
        # docstring inherited
        if self._idle_draw_id != 0:
            return
        def idle_draw(*args):
            try:
                self.draw()
            finally:
                self._idle_draw_id = 0
            return False
        self._idle_draw_id = GLib.idle_add(idle_draw)

    def flush_events(self):
        # docstring inherited
        context = GLib.MainContext.default()
        while context.pending():
            context.iteration(True)
