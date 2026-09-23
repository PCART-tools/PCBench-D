class FigureCanvasTk(FigureCanvasBase):
    keyvald = {65507 : 'control',
               65505 : 'shift',
               65513 : 'alt',
               65515 : 'super',
               65508 : 'control',
               65506 : 'shift',
               65514 : 'alt',
               65361 : 'left',
               65362 : 'up',
               65363 : 'right',
               65364 : 'down',
               65307 : 'escape',
               65470 : 'f1',
               65471 : 'f2',
               65472 : 'f3',
               65473 : 'f4',
               65474 : 'f5',
               65475 : 'f6',
               65476 : 'f7',
               65477 : 'f8',
               65478 : 'f9',
               65479 : 'f10',
               65480 : 'f11',
               65481 : 'f12',
               65300 : 'scroll_lock',
               65299 : 'break',
               65288 : 'backspace',
               65293 : 'enter',
               65379 : 'insert',
               65535 : 'delete',
               65360 : 'home',
               65367 : 'end',
               65365 : 'pageup',
               65366 : 'pagedown',
               65438 : '0',
               65436 : '1',
               65433 : '2',
               65435 : '3',
               65430 : '4',
               65437 : '5',
               65432 : '6',
               65429 : '7',
               65431 : '8',
               65434 : '9',
               65451 : '+',
               65453 : '-',
               65450 : '*',
               65455 : '/',
               65439 : 'dec',
               65421 : 'enter',
               }

    _keycode_lookup = {
                       262145: 'control',
                       524320: 'alt',
                       524352: 'alt',
                       1048584: 'super',
                       1048592: 'super',
                       131074: 'shift',
                       131076: 'shift',
                       }
    """_keycode_lookup is used for badly mapped (i.e. no event.key_sym set)
       keys on apple keyboards."""

    def __init__(self, figure, master=None, resize_callback=None):
        super(FigureCanvasTk, self).__init__(figure)
        self._idle = True
        self._idle_callback = None
        t1,t2,w,h = self.figure.bbox.bounds
        w, h = int(w), int(h)
        self._tkcanvas = Tk.Canvas(
            master=master, background="white",
            width=w, height=h, borderwidth=0, highlightthickness=0)
        self._tkphoto = Tk.PhotoImage(
            master=self._tkcanvas, width=w, height=h)
        self._tkcanvas.create_image(w//2, h//2, image=self._tkphoto)
        self._resize_callback = resize_callback
        self._tkcanvas.bind("<Configure>", self.resize)
        self._tkcanvas.bind("<Key>", self.key_press)
        self._tkcanvas.bind("<Motion>", self.motion_notify_event)
        self._tkcanvas.bind("<Enter>", self.enter_notify_event)
        self._tkcanvas.bind("<Leave>", self.leave_notify_event)
        self._tkcanvas.bind("<KeyRelease>", self.key_release)
        for name in "<Button-1>", "<Button-2>", "<Button-3>":
            self._tkcanvas.bind(name, self.button_press_event)
        for name in "<Double-Button-1>", "<Double-Button-2>", "<Double-Button-3>":
            self._tkcanvas.bind(name, self.button_dblclick_event)
        for name in "<ButtonRelease-1>", "<ButtonRelease-2>", "<ButtonRelease-3>":
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
        def filter_destroy(evt):
            if evt.widget is self._tkcanvas:
                self._master.update_idletasks()
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
        winch = width/dpival
        hinch = height/dpival
        self.figure.set_size_inches(winch, hinch, forward=False)


        self._tkcanvas.delete(self._tkphoto)
        self._tkphoto = Tk.PhotoImage(
            master=self._tkcanvas, width=int(width), height=int(height))
        self._tkcanvas.create_image(int(width/2),int(height/2),image=self._tkphoto)
        self.resize_event()
        self.draw()

        # a resizing will in general move the pointer position
        # relative to the canvas, so process it as a motion notify
        # event.  An intended side effect of this call is to allow
        # window raises (which trigger a resize) to get the cursor
        # position to the mpl event framework so key presses which are
        # over the axes will work w/o clicks or explicit motion
        self._update_pointer_position(event)

    def _update_pointer_position(self, guiEvent=None):
        """
        Figure out if we are inside the canvas or not and update the
        canvas enter/leave events
        """
        # if the pointer if over the canvas, set the lastx and lasty
        # attrs of the canvas so it can process event w/o mouse click
        # or move

        # the window's upper, left coords in screen coords
        xw = self._tkcanvas.winfo_rootx()
        yw = self._tkcanvas.winfo_rooty()
        # the pointer's location in screen coords
        xp, yp = self._tkcanvas.winfo_pointerxy()

        # not figure out the canvas coordinates of the pointer
        xc = xp - xw
        yc = yp - yw

        # flip top/bottom
        yc = self.figure.bbox.height - yc

        # JDH: this method was written originally to get the pointer
        # location to the backend lastx and lasty attrs so that events
        # like KeyEvent can be handled without mouse events.  e.g., if
        # the cursor is already above the axes, then key presses like
        # 'g' should toggle the grid.  In order for this to work in
        # backend_bases, the canvas needs to know _lastx and _lasty.
        # There are three ways to get this info the canvas:
        #
        # 1) set it explicitly
        #
        # 2) call enter/leave events explicitly.  The downside of this
        #    in the impl below is that enter could be repeatedly
        #    triggered if the mouse is over the axes and one is
        #    resizing with the keyboard.  This is not entirely bad,
        #    because the mouse position relative to the canvas is
        #    changing, but it may be surprising to get repeated entries
        #    without leaves
        #
        # 3) process it as a motion notify event.  This also has pros
        #    and cons.  The mouse is moving relative to the window, but
        #    this may surpise an event handler writer who is getting
        #   motion_notify_events even if the mouse has not moved

        # here are the three scenarios
        if 1:
            # just manually set it
            self._lastx, self._lasty = xc, yc
        elif 0:
            # alternate implementation: process it as a motion
            FigureCanvasBase.motion_notify_event(self, xc, yc, guiEvent)
        elif 0:
            # alternate implementation -- process enter/leave events
            # instead of motion/notify
            if self.figure.bbox.contains(xc, yc):
                self.enter_notify_event(guiEvent, xy=(xc,yc))
            else:
                self.leave_notify_event(guiEvent)

    def draw_idle(self):
        'update drawing area only if idle'
        if self._idle is False:
            return

        self._idle = False

        def idle_draw(*args):
            try:
                self.draw()
            finally:
                self._idle = True

        self._idle_callback = self._tkcanvas.after_idle(idle_draw)

    def get_tk_widget(self):
        """returns the Tk widget used to implement FigureCanvasTkAgg.
        Although the initial implementation uses a Tk canvas,  this routine
        is intended to hide that fact.
        """
        return self._tkcanvas

    def motion_notify_event(self, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)

    def enter_notify_event(self, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))

    def button_press_event(self, event, dblclick=False):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        num = getattr(event, 'num', None)

        if sys.platform == 'darwin':
            # 2 and 3 were reversed on the OSX platform I tested under tkagg.
            if num == 2: num = 3
            elif num == 3: num = 2

        FigureCanvasBase.button_press_event(self, x, y, num, dblclick=dblclick, guiEvent=event)

    def button_dblclick_event(self,event):
        self.button_press_event(event,dblclick=True)

    def button_release_event(self, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y

        num = getattr(event, 'num', None)

        if sys.platform == 'darwin':
            # 2 and 3 were reversed on the OSX platform I tested under tkagg.
            if num == 2: num = 3
            elif num == 3: num = 2

        FigureCanvasBase.button_release_event(self, x, y, num, guiEvent=event)

    def scroll_event(self, event):
        x = event.x
        y = self.figure.bbox.height - event.y
        num = getattr(event, 'num', None)
        if   num==4: step = +1
        elif num==5: step = -1
        else:        step =  0

        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)

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
        val = event.keysym_num
        if val in self.keyvald:
            key = self.keyvald[val]
        elif (val == 0 and sys.platform == 'darwin'
              and event.keycode in self._keycode_lookup):
            key = self._keycode_lookup[event.keycode]
        elif val < 256:
            key = chr(val)
        else:
            key = None

        # add modifier keys to the key string. Bit details originate from
        # http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        # BIT_SHIFT = 0x001; BIT_CAPSLOCK = 0x002; BIT_CONTROL = 0x004;
        # BIT_LEFT_ALT = 0x008; BIT_NUMLOCK = 0x010; BIT_RIGHT_ALT = 0x080;
        # BIT_MB_1 = 0x100; BIT_MB_2 = 0x200; BIT_MB_3 = 0x400;
        # In general, the modifier key is excluded from the modifier flag,
        # however this is not the case on "darwin", so double check that
        # we aren't adding repeat modifier flags to a modifier key.
        if sys.platform == 'win32':
            modifiers = [(17, 'alt', 'alt'),
                         (2, 'ctrl', 'control'),
                         ]
        elif sys.platform == 'darwin':
            modifiers = [(3, 'super', 'super'),
                         (4, 'alt', 'alt'),
                         (2, 'ctrl', 'control'),
                         ]
        else:
            modifiers = [(6, 'super', 'super'),
                         (3, 'alt', 'alt'),
                         (2, 'ctrl', 'control'),
                         ]

        if key is not None:
            # note, shift is not added to the keys as this is already accounted for
            for bitmask, prefix, key_name in modifiers:
                if event.state & (1 << bitmask) and key_name not in key:
                    key = '{0}+{1}'.format(prefix, key)

        return key

    def key_press(self, event):
        key = self._get_key(event)
        FigureCanvasBase.key_press_event(self, key, guiEvent=event)

    def key_release(self, event):
        key = self._get_key(event)
        FigureCanvasBase.key_release_event(self, key, guiEvent=event)

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
        return TimerTk(self._tkcanvas, *args, **kwargs)

    def flush_events(self):
        self._master.update()
