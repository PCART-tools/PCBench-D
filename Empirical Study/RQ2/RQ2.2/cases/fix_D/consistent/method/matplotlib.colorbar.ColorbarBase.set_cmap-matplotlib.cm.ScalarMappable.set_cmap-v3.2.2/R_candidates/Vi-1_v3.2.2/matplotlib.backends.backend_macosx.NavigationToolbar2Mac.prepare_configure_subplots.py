    def prepare_configure_subplots(self):
        toolfig = Figure(figsize=(6, 3))
        canvas = FigureCanvasMac(toolfig)
        toolfig.subplots_adjust(top=0.9)
        # Need to keep a reference to the tool.
        _tool = SubplotTool(self.canvas.figure, toolfig)
        return canvas
