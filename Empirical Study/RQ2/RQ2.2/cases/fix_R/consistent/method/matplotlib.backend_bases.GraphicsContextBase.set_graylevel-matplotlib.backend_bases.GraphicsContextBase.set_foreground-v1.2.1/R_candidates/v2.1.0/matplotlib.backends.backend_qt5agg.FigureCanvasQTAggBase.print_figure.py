    def print_figure(self, *args, **kwargs):
        super(FigureCanvasQTAggBase, self).print_figure(*args, **kwargs)
        self.draw()
