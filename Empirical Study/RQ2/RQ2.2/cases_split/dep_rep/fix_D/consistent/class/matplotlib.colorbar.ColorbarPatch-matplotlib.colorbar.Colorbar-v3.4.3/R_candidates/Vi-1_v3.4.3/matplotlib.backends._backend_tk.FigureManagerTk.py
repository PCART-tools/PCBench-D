class FigureManagerTk(FigureManagerBase):
    """
    Attributes
    ----------
    canvas : `FigureCanvas`
        The FigureCanvas instance
    num : int or str
        The Figure number
    toolbar : tk.Toolbar
        The tk.Toolbar
    window : tk.Window
        The tk.Window
    """

    _owns_mainloop = False

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

        self._shown = False

    def _get_toolbar(self):
        if mpl.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        elif mpl.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarTk(self.toolmanager, self.window)
        else:
            toolbar = None
        return toolbar

    def resize(self, width, height):
        max_size = 1_400_000  # the measured max on xorg 1.20.8 was 1_409_023

        if (width > max_size or height > max_size) and sys.platform == 'linux':
            raise ValueError(
                'You have requested to resize the '
                f'Tk window to ({width}, {height}), one of which '
                f'is bigger than {max_size}.  At larger sizes xorg will '
                'either exit with an error on newer versions (~1.20) or '
                'cause corruption on older version (~1.19).  We '
                'do not expect a window over a million pixel wide or tall '
                'to be intended behavior.')
        self.canvas._tkcanvas.configure(width=width, height=height)

    def show(self):
        with _restore_foreground_window_at_end():
            if not self._shown:
                def destroy(*args):
                    Gcf.destroy(self)
                self.window.protocol("WM_DELETE_WINDOW", destroy)
                self.window.deiconify()
            else:
                self.canvas.draw_idle()
            if mpl.rcParams['figure.raise_window']:
                self.canvas.manager.window.attributes('-topmost', 1)
                self.canvas.manager.window.attributes('-topmost', 0)
            self._shown = True

    def destroy(self, *args):
        if self.canvas._idle_callback:
            self.canvas._tkcanvas.after_cancel(self.canvas._idle_callback)
        if self.canvas._event_loop_id:
            self.canvas._tkcanvas.after_cancel(self.canvas._event_loop_id)

        # NOTE: events need to be flushed before issuing destroy (GH #9956),
        # however, self.window.update() can break user code. This is the
        # safest way to achieve a complete draining of the event queue,
        # but it may require users to update() on their own to execute the
        # completion in obscure corner cases.
        def delayed_destroy():
            self.window.destroy()

            if self._owns_mainloop and not Gcf.get_num_fig_managers():
                self.window.quit()

        # "after idle after 0" avoids Tcl error/race (GH #19940)
        self.window.after_idle(self.window.after, 0, delayed_destroy)

    def get_window_title(self):
        return self.window.wm_title()

    def set_window_title(self, title):
        self.window.wm_title(title)

    def full_screen_toggle(self):
        is_fullscreen = bool(self.window.attributes('-fullscreen'))
        self.window.attributes('-fullscreen', not is_fullscreen)
