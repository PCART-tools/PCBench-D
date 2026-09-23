    def prepare_configure_subplots(self):
        toolfig = Figure(figsize=(6,3))
        canvas = FigureCanvasMac(toolfig)
        toolfig.subplots_adjust(top=0.9)
        tool = SubplotTool(self.canvas.figure, toolfig)
        return canvas
