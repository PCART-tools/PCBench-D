class ConfigureSubplotsTk(backend_tools.ConfigureSubplotsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = None

    def trigger(self, *args):
        self.init_window()
        self.window.lift()

    def init_window(self):
        if self.window:
            return

        toolfig = Figure(figsize=(6, 3))
        self.window = tk.Tk()

        canvas = type(self.canvas)(toolfig, master=self.window)
        toolfig.subplots_adjust(top=0.9)
        SubplotTool(self.figure, toolfig)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self, *args, **kwargs):
        if self.window is not None:
            self.window.destroy()
            self.window = None
