    def __init__(self, cs):
        self.cs = cs
        BlockingMouseInput.__init__(self, fig=cs.ax.figure)
