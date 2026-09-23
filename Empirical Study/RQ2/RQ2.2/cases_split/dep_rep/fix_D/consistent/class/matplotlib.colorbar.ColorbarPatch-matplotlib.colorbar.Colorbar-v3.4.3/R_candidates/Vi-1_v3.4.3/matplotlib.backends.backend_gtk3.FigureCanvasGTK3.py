class FigureCanvasGTK3(Gtk.DrawingArea, FigureCanvasBase):
    required_interactive_framework = "gtk3"
    _timer_cls = TimerGTK3
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
                  | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                  | Gdk.EventMask.SCROLL_MASK)

    def __init__(self, figure=None):
        FigureCanvasBase.__init__(self, figure)
        GObject.GObject.__init__(self)

        self._idle_draw_id = 0
        self._lastCursor = None
        self._rubberband_rect = None

        self.connect('scroll_event',         self.scroll_event)
        self.connect('button_press_event',   self.button_press_event)
        self.connect('button_release_event', self.button_release_event)
        self.connect('configure_event',      self.configure_event)
        self.connect('draw',                 self.on_draw_event)
        self.connect('draw',                 self._post_draw)
        self.connect('key_press_event',      self.key_press_event)
        self.connect('key_release_event',    self.key_release_event)
        self.connect('motion_notify_event',  self.motion_notify_event)
        self.connect('leave_notify_event',   self.leave_notify_event)
        self.connect('enter_notify_event',   self.enter_notify_event)
        self.connect('size_allocate',        self.size_allocate)

        self.set_events(self.__class__.event_mask)

        self.set_can_focus(True)

        css = Gtk.CssProvider()
        css.load_from_data(b".matplotlib-canvas { background-color: white; }")
        style_ctx = self.get_style_context()
        style_ctx.add_provider(css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        style_ctx.add_class("matplotlib-canvas")

        renderer_init = _api.deprecate_method_override(
            __class__._renderer_init, self, allow_empty=True, since="3.3",
            addendum="Please initialize the renderer, if needed, in the "
            "subclass' __init__; a fully empty _renderer_init implementation "
            "may be kept for compatibility with earlier versions of "
            "Matplotlib.")
        if renderer_init:
            renderer_init()

    @_api.deprecated("3.3", alternative="__init__")
    def _renderer_init(self):
        pass

    def destroy(self):
        #Gtk.DrawingArea.destroy(self)
        self.close_event()

    def scroll_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        step = 1 if event.direction == Gdk.ScrollDirection.UP else -1
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)
        return False  # finish event propagation?

    def button_press_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        FigureCanvasBase.button_press_event(
            self, x, y, event.button, guiEvent=event)
        return False  # finish event propagation?

    def button_release_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        FigureCanvasBase.button_release_event(
            self, x, y, event.button, guiEvent=event)
        return False  # finish event propagation?

    def key_press_event(self, widget, event):
        key = self._get_key(event)
        FigureCanvasBase.key_press_event(self, key, guiEvent=event)
        return True  # stop event propagation

    def key_release_event(self, widget, event):
        key = self._get_key(event)
        FigureCanvasBase.key_release_event(self, key, guiEvent=event)
        return True  # stop event propagation

    def motion_notify_event(self, widget, event):
        if event.is_hint:
            t, x, y, state = event.window.get_device_position(event.device)
        else:
            x, y = event.x, event.y

        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - y
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)
        return False  # finish event propagation?

    def leave_notify_event(self, widget, event):
        FigureCanvasBase.leave_notify_event(self, event)

    def enter_notify_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))

    def size_allocate(self, widget, allocation):
        dpival = self.figure.dpi
        winch = allocation.width / dpival
        hinch = allocation.height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)
        FigureCanvasBase.resize_event(self)
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
                    key = '{0}+{1}'.format(prefix, key)
        return key

    def configure_event(self, widget, event):
        if widget.get_property("window") is None:
            return
        w, h = event.width, event.height
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

        x0, y0, w, h = self._rubberband_rect
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
        Gdk.threads_enter()
        while Gtk.events_pending():
            Gtk.main_iteration()
        Gdk.flush()
        Gdk.threads_leave()
