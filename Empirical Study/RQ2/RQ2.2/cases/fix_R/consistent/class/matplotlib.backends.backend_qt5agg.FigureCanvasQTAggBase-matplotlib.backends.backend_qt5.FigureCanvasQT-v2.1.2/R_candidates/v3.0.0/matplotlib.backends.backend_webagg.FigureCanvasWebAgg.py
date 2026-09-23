class FigureCanvasWebAgg(core.FigureCanvasWebAggCore):
    def show(self):
        # show the figure window
        global show  # placates pyflakes: created by @_Backend.export below
        show()

    def new_timer(self, *args, **kwargs):
        return TimerTornado(*args, **kwargs)
