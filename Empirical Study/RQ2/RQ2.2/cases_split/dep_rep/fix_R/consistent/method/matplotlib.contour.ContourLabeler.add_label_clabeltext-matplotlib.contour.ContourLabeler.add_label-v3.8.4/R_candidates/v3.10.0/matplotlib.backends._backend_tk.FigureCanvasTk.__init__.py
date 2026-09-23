    def __init__(self, figure=None, master=None):
        super().__init__(figure)
        self._idle_draw_id = None
        self._event_loop_id = None
        w, h = self.get_width_height(physical=True)
        self._tkcanvas = tk.Canvas(
            master=master, background="white",
            width=w, height=h, borderwidth=0, highlightthickness=0)
        self._tkphoto = tk.PhotoImage(
            master=self._tkcanvas, width=w, height=h)
        self._tkcanvas_image_region = self._tkcanvas.create_image(
            w//2, h//2, image=self._tkphoto)
        self._tkcanvas.bind("<Configure>", self.resize)
        self._tkcanvas.bind("<Map>", self._update_device_pixel_ratio)
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
        # See https://wiki.tcl-lang.org/3893 (mousewheel) for details
        root = self._tkcanvas.winfo_toplevel()

        # Prevent long-lived references via tkinter callback structure GH-24820
        weakself = weakref.ref(self)
        weakroot = weakref.ref(root)

        def scroll_event_windows(event):
            self = weakself()
            if self is None:
                root = weakroot()
                if root is not None:
                    root.unbind("<MouseWheel>", scroll_event_windows_id)
                return
            return self.scroll_event_windows(event)
        scroll_event_windows_id = root.bind("<MouseWheel>", scroll_event_windows, "+")

        # Can't get destroy events by binding to _tkcanvas. Therefore, bind
        # to the window and filter.
        def filter_destroy(event):
            self = weakself()
            if self is None:
                root = weakroot()
                if root is not None:
                    root.unbind("<Destroy>", filter_destroy_id)
                return
            if event.widget is self._tkcanvas:
                CloseEvent("close_event", self)._process()
        filter_destroy_id = root.bind("<Destroy>", filter_destroy, "+")

        self._tkcanvas.focus_set()

        self._rubberband_rect_black = None
        self._rubberband_rect_white = None
