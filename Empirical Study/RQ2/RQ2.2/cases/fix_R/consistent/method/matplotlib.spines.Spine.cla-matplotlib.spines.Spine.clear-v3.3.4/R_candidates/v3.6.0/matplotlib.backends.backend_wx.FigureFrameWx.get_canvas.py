    @_api.deprecated(
        "3.6", alternative="the canvas_class constructor parameter")
    def get_canvas(self, fig):
        return FigureCanvasWx(self, -1, fig)
