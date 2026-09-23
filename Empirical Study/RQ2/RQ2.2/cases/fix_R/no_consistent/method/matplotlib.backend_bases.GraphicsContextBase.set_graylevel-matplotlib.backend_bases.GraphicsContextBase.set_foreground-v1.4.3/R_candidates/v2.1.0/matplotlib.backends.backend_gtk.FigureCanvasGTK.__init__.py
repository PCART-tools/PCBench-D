    def __init__(self, figure):
        if self.__class__ == matplotlib.backends.backend_gtk.FigureCanvasGTK:
            warn_deprecated('2.0', message="The GTK backend is "
                            "deprecated. It is untested, known to be "
                            "broken and will be removed in Matplotlib 2.2. "
                            "Use the GTKAgg backend instead. "
                            "See Matplotlib usage FAQ for"
                            " more info on backends.",
                            alternative="GTKAgg")
        FigureCanvasBase.__init__(self, figure)
        gtk.DrawingArea.__init__(self)

        self._idle_draw_id  = 0
        self._need_redraw   = True
        self._pixmap_width  = -1
        self._pixmap_height = -1
        self._lastCursor    = None

        self.connect('scroll_event',         self.scroll_event)
        self.connect('button_press_event',   self.button_press_event)
        self.connect('button_release_event', self.button_release_event)
        self.connect('configure_event',      self.configure_event)
        self.connect('expose_event',         self.expose_event)
        self.connect('key_press_event',      self.key_press_event)
        self.connect('key_release_event',    self.key_release_event)
        self.connect('motion_notify_event',  self.motion_notify_event)
        self.connect('leave_notify_event',   self.leave_notify_event)
        self.connect('enter_notify_event',   self.enter_notify_event)

        self.set_events(self.__class__.event_mask)

        self.set_double_buffered(False)
        self.set_flags(gtk.CAN_FOCUS)
        self._renderer_init()

        self.last_downclick = {}
