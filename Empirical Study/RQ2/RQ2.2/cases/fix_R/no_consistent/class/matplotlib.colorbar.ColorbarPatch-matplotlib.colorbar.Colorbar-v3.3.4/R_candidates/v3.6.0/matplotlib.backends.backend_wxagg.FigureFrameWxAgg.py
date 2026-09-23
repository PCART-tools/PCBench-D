@_api.deprecated(
    "3.6", alternative="FigureFrameWx(..., canvas_class=FigureCanvasWxAgg)")
class FigureFrameWxAgg(FigureFrameWx):
    def get_canvas(self, fig):
        return FigureCanvasWxAgg(self, -1, fig)
