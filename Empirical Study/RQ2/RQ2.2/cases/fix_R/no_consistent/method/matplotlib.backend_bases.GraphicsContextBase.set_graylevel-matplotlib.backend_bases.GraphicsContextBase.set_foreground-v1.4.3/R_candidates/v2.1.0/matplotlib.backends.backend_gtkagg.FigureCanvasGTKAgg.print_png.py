    def print_png(self, filename, *args, **kwargs):
        # Do this so we can save the resolution of figure in the PNG file
        agg = self.switch_backends(FigureCanvasAgg)
        return agg.print_png(filename, *args, **kwargs)
