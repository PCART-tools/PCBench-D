@_api.deprecated(
    "3.6", alternative="FigureFrameWx(..., canvas_class=FigureCanvasWxCairo)")
class FigureFrameWxCairo(FigureFrameWx):
    def get_canvas(self, fig):
        return FigureCanvasWxCairo(self, -1, fig)
