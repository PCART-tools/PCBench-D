class FigureCanvasTk(FigureCanvasBase):
    required_interactive_framework = "tk"

    @_api.delete_parameter(
        "3.4", "resize_callback",
        alternative="get_tk_widget().bind('<Configure>', ..., True)")
    def __init__(self, figure=None, master=None, resize_callback=None):
        super().__init__(figure)
        self._idle = True
        self._idle_callback = None
        self._event_loop_id = None
        w, h = self.figure.bbox.size.astype(int)
        self._tkcanvas = tk.Canvas(
            master=master, background="white",
            width=w, height=h, borderwidth=0, highlightthickness=0)
        self._tkphoto = tk.PhotoImage(
            master=self._tkcanvas, width=w, height=h)
        self._tkcanvas.create_image(w//2, h//2, image=self._tkphoto)
        self._resize_callback = resize_callback
        self._tkcanvas.bind("<Configure>", self.resize)
        self._tkcanvas.bind("<Key>", self.key_press)
        self._tkcanvas.bind("<Motion>", self.motion_notify_event)
        self._tkcanvas.bind("<Enter>", self.enter_notify_event)
        self._tkcanvas.bind("<Leave>", self.leave_notify_event)
        self._tkcanvas.bind("<KeyRelease>", self.key_release)
        for name in ["<Button-1>", "<Button-2>", "<Button-3>"]:
            self._tkcanvas.bind(name, self.button_press_event)
        for name in [
                "<Double-Button-1>", "<Double-Button-2>", "<Double-Button-3>"]:
            self._tkcanvas.bind(name, self.button_dblclick_event)
        for name in [
                "<ButtonRelease-1>", "<ButtonRelease-2>", "<ButtonRelease-3>"]:
            self._tkcanvas.bind(name, self.button_release_event)

        # Mouse wheel on Linux generates button 4/5 events
        for name in "<Button-4>", "<Button-5>":
            self._tkcanvas.bind(name, self.scroll_event)
        # Mouse wheel for windows goes to the window with the focus.
        # Since the canvas won't usually have the focus, bind the
        # event to the window containing the canvas instead.
        # See http://wiki.tcl.tk/3893 (mousewheel) for details
        root = self._tkcanvas.winfo_toplevel()
        root.bind("<MouseWheel>", self.scroll_event_windows, "+")

        # Can't get destroy events by binding to _tkcanvas. Therefore, bind
        # to the window and filter.
        def filter_destroy(event):
            if event.widget is self._tkcanvas:
                self.close_event()
        root.bind("<Destroy>", filter_destroy, "+")

        self._master = master
        self._tkcanvas.focus_set()

    def resize(self, event):
        width, height = event.width, event.height
        if self._resize_callback is not None:
            self._resize_callback(event)

        # compute desired figure size in inches
        dpival = self.figure.dpi
        winch = width / dpival
        hinch = height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)

        self._tkcanvas.delete(self._tkphoto)
        self._tkphoto = tk.PhotoImage(
            master=self._tkcanvas, width=int(width), height=int(height))
        self._tkcanvas.create_image(
            int(width / 2), int(height / 2), image=self._tkphoto)
        self.resize_event()

    def draw_idle(self):
        # docstring inherited
        if not self._idle:
            return

        self._idle = False

        def idle_draw(*args):
            try:
                self.draw()
            finally:
                self._idle = True

        self._idle_callback = self._tkcanvas.after_idle(idle_draw)

    def get_tk_widget(self):
        """
        Return the Tk widget used to implement FigureCanvasTkAgg.

        Although the initial implementation uses a Tk canvas,  this routine
        is intended to hide that fact.
        """
        return self._tkcanvas

    def motion_notify_event(self, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        super().motion_notify_event(x, y, guiEvent=event)

    def enter_notify_event(self, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        super().enter_notify_event(guiEvent=event, xy=(x, y))

    def button_press_event(self, event, dblclick=False):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        num = getattr(event, 'num', None)

        if sys.platform == 'darwin':
            # 2 and 3 were reversed on the OSX platform I tested under tkagg.
            if num == 2:
                num = 3
            elif num == 3:
                num = 2

        super().button_press_event(x, y, num,
                                   dblclick=dblclick, guiEvent=event)

    def button_dblclick_event(self, event):
        self.button_press_event(event, dblclick=True)

    def button_release_event(self, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y

        num = getattr(event, 'num', None)

        if sys.platform == 'darwin':
            # 2 and 3 were reversed on the OSX platform I tested under tkagg.
            if num == 2:
                num = 3
            elif num == 3:
                num = 2

        super().button_release_event(x, y, num, guiEvent=event)

    def scroll_event(self, event):
        x = event.x
        y = self.figure.bbox.height - event.y
        num = getattr(event, 'num', None)
        step = 1 if num == 4 else -1 if num == 5 else 0
        super().scroll_event(x, y, step, guiEvent=event)

    def scroll_event_windows(self, event):
        """MouseWheel event processor"""
        # need to find the window that contains the mouse
        w = event.widget.winfo_containing(event.x_root, event.y_root)
        if w == self._tkcanvas:
            x = event.x_root - w.winfo_rootx()
            y = event.y_root - w.winfo_rooty()
            y = self.figure.bbox.height - y
            step = event.delta/120.
            FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)

    def _get_key(self, event):
        unikey = event.char
        key = cbook._unikey_or_keysym_to_mplkey(unikey, event.keysym)

        # add modifier keys to the key string. Bit details originate from
        # http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        # BIT_SHIFT = 0x001; BIT_CAPSLOCK = 0x002; BIT_CONTROL = 0x004;
        # BIT_LEFT_ALT = 0x008; BIT_NUMLOCK = 0x010; BIT_RIGHT_ALT = 0x080;
        # BIT_MB_1 = 0x100; BIT_MB_2 = 0x200; BIT_MB_3 = 0x400;
        # In general, the modifier key is excluded from the modifier flag,
        # however this is not the case on "darwin", so double check that
        # we aren't adding repeat modifier flags to a modifier key.
        if sys.platform == 'win32':
            modifiers = [(2, 'ctrl', 'control'),
                         (17, 'alt', 'alt'),
                         (0, 'shift', 'shift'),
                         ]
        elif sys.platform == 'darwin':
            modifiers = [(2, 'ctrl', 'control'),
                         (4, 'alt', 'alt'),
                         (0, 'shift', 'shift'),
                         (3, 'super', 'super'),
                         ]
        else:
            modifiers = [(2, 'ctrl', 'control'),
                         (3, 'alt', 'alt'),
                         (0, 'shift', 'shift'),
                         (6, 'super', 'super'),
                         ]

        if key is not None:
            # shift is not added to the keys as this is already accounted for
            for bitmask, prefix, key_name in modifiers:
                if event.state & (1 << bitmask) and key_name not in key:
                    if not (prefix == 'shift' and unikey):
                        key = '{0}+{1}'.format(prefix, key)

        return key

    def key_press(self, event):
        key = self._get_key(event)
        FigureCanvasBase.key_press_event(self, key, guiEvent=event)

    def key_release(self, event):
        key = self._get_key(event)
        FigureCanvasBase.key_release_event(self, key, guiEvent=event)

    def new_timer(self, *args, **kwargs):
        # docstring inherited
        return TimerTk(self._tkcanvas, *args, **kwargs)

    def flush_events(self):
        # docstring inherited
        self._master.update()

    def start_event_loop(self, timeout=0):
        # docstring inherited
        if timeout > 0:
            milliseconds = int(1000 * timeout)
            if milliseconds > 0:
                self._event_loop_id = self._tkcanvas.after(
                    milliseconds, self.stop_event_loop)
            else:
                self._event_loop_id = self._tkcanvas.after_idle(
                    self.stop_event_loop)
        self._master.mainloop()

    def stop_event_loop(self):
        # docstring inherited
        if self._event_loop_id:
            self._master.after_cancel(self._event_loop_id)
            self._event_loop_id = None
        self._master.quit()
