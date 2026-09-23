    def init_window(self):
        if self.window:
            return

        toolfig = Figure(figsize=(6, 3))
        self.window = Tk.Tk()

        canvas = FigureCanvasTkAgg(toolfig, master=self.window)
        toolfig.subplots_adjust(top=0.9)
        _tool = SubplotTool(self.figure, toolfig)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)
