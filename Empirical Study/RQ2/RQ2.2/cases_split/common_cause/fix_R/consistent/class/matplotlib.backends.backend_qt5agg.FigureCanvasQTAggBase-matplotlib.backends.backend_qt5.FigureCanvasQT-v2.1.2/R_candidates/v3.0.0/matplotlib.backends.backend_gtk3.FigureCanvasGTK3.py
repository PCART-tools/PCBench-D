class FigureCanvasGTK3(Gtk.DrawingArea, FigureCanvasBase):
    keyvald = {65507: 'control',
               65505: 'shift',
               65513: 'alt',
               65508: 'control',
               65506: 'shift',
               65514: 'alt',
               65361: 'left',
               65362: 'up',
               65363: 'right',
               65364: 'down',
               65307: 'escape',
               65470: 'f1',
               65471: 'f2',
               65472: 'f3',
               65473: 'f4',
               65474: 'f5',
               65475: 'f6',
               65476: 'f7',
               65477: 'f8',
               65478: 'f9',
               65479: 'f10',
               65480: 'f11',
               65481: 'f12',
               65300: 'scroll_lock',
               65299: 'break',
               65288: 'backspace',
               65293: 'enter',
               65379: 'insert',
               65535: 'delete',
               65360: 'home',
               65367: 'end',
               65365: 'pageup',
               65366: 'pagedown',
               65438: '0',
               65436: '1',
               65433: '2',
               65435: '3',
               65430: '4',
               65437: '5',
               65432: '6',
               65429: '7',
               65431: '8',
               65434: '9',
               65451: '+',
               65453: '-',
               65450: '*',
               65455: '/',
               65439: 'dec',
               65421: 'enter',
               }

    # Setting this as a static constant prevents
    # this resulting expression from leaking
    event_mask = (Gdk.EventMask.BUTTON_PRESS_MASK   |
                  Gdk.EventMask.BUTTON_RELEASE_MASK |
                  Gdk.EventMask.EXPOSURE_MASK       |
                  Gdk.EventMask.KEY_PRESS_MASK      |
                  Gdk.EventMask.KEY_RELEASE_MASK    |
                  Gdk.EventMask.ENTER_NOTIFY_MASK   |
                  Gdk.EventMask.LEAVE_NOTIFY_MASK   |
                  Gdk.EventMask.POINTER_MOTION_MASK |
                  Gdk.EventMask.POINTER_MOTION_HINT_MASK|
                  Gdk.EventMask.SCROLL_MASK)

    def __init__(self, figure):
        FigureCanvasBase.__init__(self, figure)
        GObject.GObject.__init__(self)

        self._idle_draw_id  = 0
        self._lastCursor    = None

        self.connect('scroll_event',         self.scroll_event)
        self.connect('button_press_event',   self.button_press_event)
        self.connect('button_release_event', self.button_release_event)
        self.connect('configure_event',      self.configure_event)
        self.connect('draw',                 self.on_draw_event)
        self.connect('key_press_event',      self.key_press_event)
        self.connect('key_release_event',    self.key_release_event)
        self.connect('motion_notify_event',  self.motion_notify_event)
        self.connect('leave_notify_event',   self.leave_notify_event)
        self.connect('enter_notify_event',   self.enter_notify_event)
        self.connect('size_allocate',        self.size_allocate)

        self.set_events(self.__class__.event_mask)

        self.set_double_buffered(True)
        self.set_can_focus(True)
        self._renderer_init()
        default_context = GLib.main_context_get_thread_default() or GLib.main_context_default()

    def destroy(self):
        #Gtk.DrawingArea.destroy(self)
        self.close_event()
        if self._idle_draw_id != 0:
            GLib.source_remove(self._idle_draw_id)

    def scroll_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        if event.direction==Gdk.ScrollDirection.UP:
            step = 1
        else:
            step = -1
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)
        return False  # finish event propagation?

    def button_press_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        FigureCanvasBase.button_press_event(self, x, y, event.button, guiEvent=event)
        return False  # finish event propagation?

    def button_release_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        FigureCanvasBase.button_release_event(self, x, y, event.button, guiEvent=event)
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
            t, x, y, state = event.window.get_pointer()
        else:
            x, y, state = event.x, event.y, event.get_state()

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
        if event.keyval in self.keyvald:
            key = self.keyvald[event.keyval]
        elif event.keyval < 256:
            key = chr(event.keyval)
        else:
            key = None

        modifiers = [
                     (Gdk.ModifierType.MOD4_MASK, 'super'),
                     (Gdk.ModifierType.MOD1_MASK, 'alt'),
                     (Gdk.ModifierType.CONTROL_MASK, 'ctrl'),
                    ]
        for key_mask, prefix in modifiers:
            if event.state & key_mask:
                key = '{0}+{1}'.format(prefix, key)

        return key

    def configure_event(self, widget, event):
        if widget.get_property("window") is None:
            return
        w, h = event.width, event.height
        if w < 3 or h < 3:
            return # empty fig
        # resize the figure (in inches)
        dpi = self.figure.dpi
        self.figure.set_size_inches(w / dpi, h / dpi, forward=False)
        return False  # finish event propagation?

    def on_draw_event(self, widget, ctx):
        # to be overwritten by GTK3Agg or GTK3Cairo
        pass

    def draw(self):
        if self.get_visible() and self.get_mapped():
            self.queue_draw()
            # do a synchronous draw (its less efficient than an async draw,
            # but is required if/when animation is used)
            self.get_property("window").process_updates(False)

    def draw_idle(self):
        if self._idle_draw_id != 0:
            return
        def idle_draw(*args):
            try:
                self.draw()
            finally:
                self._idle_draw_id = 0
            return False
        self._idle_draw_id = GLib.idle_add(idle_draw)

    def new_timer(self, *args, **kwargs):
        """
        Creates a new backend-specific subclass of :class:`backend_bases.Timer`.
        This is useful for getting periodic events through the backend's native
        event loop. Implemented only for backends with GUIs.

        Other Parameters
        ----------------
        interval : scalar
            Timer interval in milliseconds
        callbacks : list
            Sequence of (func, args, kwargs) where ``func(*args, **kwargs)``
            will be executed by the timer every *interval*.
        """
        return TimerGTK3(*args, **kwargs)

    def flush_events(self):
        Gdk.threads_enter()
        while Gtk.events_pending():
            Gtk.main_iteration()
        Gdk.flush()
        Gdk.threads_leave()
