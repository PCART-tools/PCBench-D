    def configure_subplots(self):
        toolfig = Figure(figsize=(6, 3))
        window = tk.Toplevel()
        canvas = type(self.canvas)(toolfig, master=window)
        toolfig.subplots_adjust(top=0.9)
        canvas.tool = SubplotTool(self.canvas.figure, toolfig)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        window.grab_set()
