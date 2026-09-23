class FigureCanvasGTK4(Gtk.DrawingArea, FigureCanvasBase):
    required_interactive_framework = "gtk4"
    supports_blit = False
    _timer_cls = TimerGTK4
    _context_is_scaled = False

    def __init__(self, figure=None):
        FigureCanvasBase.__init__(self, figure)
        GObject.GObject.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)

        self._idle_draw_id = 0
        self._lastCursor = None
        self._rubberband_rect = None

        self.set_draw_func(self._draw_func)
        self.connect('resize', self.resize_event)
        self.connect('notify::scale-factor', self._update_device_pixel_ratio)

        click = Gtk.GestureClick()
        click.set_button(0)  # All buttons.
        click.connect('pressed', self.button_press_event)
        click.connect('released', self.button_release_event)
        self.add_controller(click)

        key = Gtk.EventControllerKey()
        key.connect('key-pressed', self.key_press_event)
        key.connect('key-released', self.key_release_event)
        self.add_controller(key)

        motion = Gtk.EventControllerMotion()
        motion.connect('motion', self.motion_notify_event)
        motion.connect('enter', self.enter_notify_event)
        motion.connect('leave', self.leave_notify_event)
        self.add_controller(motion)

        scroll = Gtk.EventControllerScroll.new(
            Gtk.EventControllerScrollFlags.VERTICAL)
        scroll.connect('scroll', self.scroll_event)
        self.add_controller(scroll)

        self.set_focusable(True)

        css = Gtk.CssProvider()
        css.load_from_data(b".matplotlib-canvas { background-color: white; }")
        style_ctx = self.get_style_context()
        style_ctx.add_provider(css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        style_ctx.add_class("matplotlib-canvas")

    def pick(self, mouseevent):
        # GtkWidget defines pick in GTK4, so we need to override here to work
        # with the base implementation we want.
        FigureCanvasBase.pick(self, mouseevent)

    def destroy(self):
        self.close_event()

    def set_cursor(self, cursor):
        # docstring inherited
        self.set_cursor_from_name(_mpl_to_gtk_cursor(cursor))

    def _mouse_event_coords(self, x, y):
        """
        Calculate mouse coordinates in physical pixels.

        GTK use logical pixels, but the figure is scaled to physical pixels for
        rendering.  Transform to physical pixels so that all of the down-stream
        transforms work as expected.

        Also, the origin is different and needs to be corrected.
        """
        x = x * self.device_pixel_ratio
        # flip y so y=0 is bottom of canvas
        y = self.figure.bbox.height - y * self.device_pixel_ratio
        return x, y

    def scroll_event(self, controller, dx, dy):
        FigureCanvasBase.scroll_event(self, 0, 0, dy)
        return True

    def button_press_event(self, controller, n_press, x, y):
        x, y = self._mouse_event_coords(x, y)
        FigureCanvasBase.button_press_event(self, x, y,
                                            controller.get_current_button())
        self.grab_focus()

    def button_release_event(self, controller, n_press, x, y):
        x, y = self._mouse_event_coords(x, y)
        FigureCanvasBase.button_release_event(self, x, y,
                                              controller.get_current_button())

    def key_press_event(self, controller, keyval, keycode, state):
        key = self._get_key(keyval, keycode, state)
        FigureCanvasBase.key_press_event(self, key)
        return True

    def key_release_event(self, controller, keyval, keycode, state):
        key = self._get_key(keyval, keycode, state)
        FigureCanvasBase.key_release_event(self, key)
        return True

    def motion_notify_event(self, controller, x, y):
        x, y = self._mouse_event_coords(x, y)
        FigureCanvasBase.motion_notify_event(self, x, y)

    def leave_notify_event(self, controller):
        FigureCanvasBase.leave_notify_event(self)

    def enter_notify_event(self, controller, x, y):
        x, y = self._mouse_event_coords(x, y)
        FigureCanvasBase.enter_notify_event(self, xy=(x, y))

    def resize_event(self, area, width, height):
        self._update_device_pixel_ratio()
        dpi = self.figure.dpi
        winch = width * self.device_pixel_ratio / dpi
        hinch = height * self.device_pixel_ratio / dpi
        self.figure.set_size_inches(winch, hinch, forward=False)
        FigureCanvasBase.resize_event(self)
        self.draw_idle()

    def _get_key(self, keyval, keycode, state):
        unikey = chr(Gdk.keyval_to_unicode(keyval))
        key = cbook._unikey_or_keysym_to_mplkey(
            unikey,
            Gdk.keyval_name(keyval))
        modifiers = [
            (Gdk.ModifierType.CONTROL_MASK, 'ctrl'),
            (Gdk.ModifierType.ALT_MASK, 'alt'),
            (Gdk.ModifierType.SHIFT_MASK, 'shift'),
            (Gdk.ModifierType.SUPER_MASK, 'super'),
        ]
        for key_mask, prefix in modifiers:
            if state & key_mask:
                if not (prefix == 'shift' and unikey.isprintable()):
                    key = f'{prefix}+{key}'
        return key

    def _update_device_pixel_ratio(self, *args, **kwargs):
        # We need to be careful in cases with mixed resolution displays if
        # device_pixel_ratio changes.
        if self._set_device_pixel_ratio(self.get_scale_factor()):
            self.draw()

    def _draw_rubberband(self, rect):
        self._rubberband_rect = rect
        # TODO: Only update the rubberband area.
        self.queue_draw()

    def _draw_func(self, drawing_area, ctx, width, height):
        self.on_draw_event(self, ctx)
        self._post_draw(self, ctx)

    def _post_draw(self, widget, ctx):
        if self._rubberband_rect is None:
            return

        lw = 1
        dash = 3
        if not self._context_is_scaled:
            x0, y0, w, h = (dim / self.device_pixel_ratio
                            for dim in self._rubberband_rect)
        else:
            x0, y0, w, h = self._rubberband_rect
            lw *= self.device_pixel_ratio
            dash *= self.device_pixel_ratio
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
        ctx.set_line_width(lw)
        ctx.set_dash((dash, dash), 0)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke_preserve()

        ctx.set_dash((dash, dash), dash)
        ctx.set_source_rgb(1, 1, 1)
        ctx.stroke()

    def on_draw_event(self, widget, ctx):
        # to be overwritten by GTK4Agg or GTK4Cairo
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
