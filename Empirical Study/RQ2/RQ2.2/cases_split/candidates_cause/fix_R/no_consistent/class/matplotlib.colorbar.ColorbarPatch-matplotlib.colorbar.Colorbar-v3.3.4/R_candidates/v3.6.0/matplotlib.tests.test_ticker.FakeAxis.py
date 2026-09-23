class FakeAxis:
    """Allow Formatter to be called without having a "full" plot set up."""
    def __init__(self, vmin=1, vmax=10):
        self.vmin = vmin
        self.vmax = vmax

    def get_view_interval(self):
        return self.vmin, self.vmax
