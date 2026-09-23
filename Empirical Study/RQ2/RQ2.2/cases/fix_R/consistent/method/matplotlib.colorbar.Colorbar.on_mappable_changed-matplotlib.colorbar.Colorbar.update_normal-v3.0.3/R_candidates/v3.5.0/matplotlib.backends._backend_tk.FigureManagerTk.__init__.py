    def __init__(self, canvas, num, window):
        self.window = window
        super().__init__(canvas, num)
        self.window.withdraw()
        # packing toolbar first, because if space is getting low, last packed
        # widget is getting shrunk first (-> the canvas)
        self.toolbar = self._get_toolbar()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)

        # If the window has per-monitor DPI awareness, then setup a Tk variable
        # to store the DPI, which will be updated by the C code, and the trace
        # will handle it on the Python side.
        window_frame = int(window.wm_frame(), 16)
        window_dpi = tk.IntVar(master=window, value=96,
                               name=f'window_dpi{window_frame}')
        if _tkagg.enable_dpi_awareness(window_frame, window.tk.interpaddr()):
            self._window_dpi = window_dpi  # Prevent garbage collection.
            window_dpi.trace_add('write', self._update_window_dpi)

        self._shown = False
