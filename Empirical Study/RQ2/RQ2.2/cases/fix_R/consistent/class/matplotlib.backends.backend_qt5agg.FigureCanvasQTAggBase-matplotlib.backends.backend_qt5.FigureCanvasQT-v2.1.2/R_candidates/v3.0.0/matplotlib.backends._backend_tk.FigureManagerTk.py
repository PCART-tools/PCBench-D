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
    def __init__(self, canvas, num, window):
        FigureManagerBase.__init__(self, canvas, num)
        self.window = window
        self.window.withdraw()
        self.set_window_title("Figure %d" % num)
        self.canvas = canvas
        # If using toolmanager it has to be present when initializing the toolbar
        self.toolmanager = self._get_toolmanager()
        # packing toolbar first, because if space is getting low, last packed widget is getting shrunk first (-> the canvas)
        self.toolbar = self._get_toolbar()
        self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self._num = num

        self.statusbar = None

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)
                self.statusbar = StatusbarTk(self.window, self.toolmanager)

        self._shown = False

    def _get_toolbar(self):
        if matplotlib.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        elif matplotlib.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarTk(self.toolmanager, self.window)
        else:
            toolbar = None
        return toolbar

    def _get_toolmanager(self):
        if rcParams['toolbar'] == 'toolmanager':
            toolmanager = ToolManager(self.canvas.figure)
        else:
            toolmanager = None
        return toolmanager

    def resize(self, width, height):
        self.canvas._tkcanvas.master.geometry("%dx%d" % (width, height))

        if self.toolbar is not None:
            self.toolbar.configure(width=width)

    def show(self):
        """
        this function doesn't segfault but causes the
        PyEval_RestoreThread: NULL state bug on win32
        """
        with _restore_foreground_window_at_end():
            if not self._shown:
                def destroy(*args):
                    self.window = None
                    Gcf.destroy(self._num)
                self.canvas._tkcanvas.bind("<Destroy>", destroy)
                self.window.deiconify()
            else:
                self.canvas.draw_idle()
            # Raise the new window.
            self.canvas.manager.window.attributes('-topmost', 1)
            self.canvas.manager.window.attributes('-topmost', 0)
            self._shown = True

    def destroy(self, *args):
        if self.window is not None:
            #self.toolbar.destroy()
            if self.canvas._idle_callback:
                self.canvas._tkcanvas.after_cancel(self.canvas._idle_callback)
            self.window.destroy()
        if Gcf.get_num_fig_managers()==0:
            if self.window is not None:
                self.window.quit()
        self.window = None

    def get_window_title(self):
        return self.window.wm_title()

    def set_window_title(self, title):
        self.window.wm_title(title)

    def full_screen_toggle(self):
        is_fullscreen = bool(self.window.attributes('-fullscreen'))
        self.window.attributes('-fullscreen', not is_fullscreen)
