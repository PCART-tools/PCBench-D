    def __init__(self, figure):
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

        self.set_double_buffered(True)
        self.set_can_focus(True)

        renderer_init = cbook._deprecate_method_override(
            __class__._renderer_init, self, allow_empty=True, since="3.3",
            addendum="Please initialize the renderer, if needed, in the "
            "subclass' __init__; a fully empty _renderer_init implementation "
            "may be kept for compatibility with earlier versions of "
            "Matplotlib.")
        if renderer_init:
            renderer_init()
