class ConfigureSubplotsTk(backend_tools.ConfigureSubplotsBase):
    def __init__(self, *args, **kwargs):
        backend_tools.ConfigureSubplotsBase.__init__(self, *args, **kwargs)
        self.window = None

    def trigger(self, *args):
        self.init_window()
        self.window.lift()

    def init_window(self):
        if self.window:
            return

        toolfig = Figure(figsize=(6, 3))
        self.window = Tk.Tk()

        canvas = type(self.canvas)(toolfig, master=self.window)
        toolfig.subplots_adjust(top=0.9)
        _tool = SubplotTool(self.figure, toolfig)
        canvas.draw()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self, *args, **kwargs):
        self.window.destroy()
        self.window = None
