    def __init__(self, c, state, math=True):
        Node.__init__(self)
        self.c = c
        self.font_output = state.font_output
        self.font = state.font
        self.font_class = state.font_class
        self.fontsize = state.fontsize
        self.dpi = state.dpi
        self.math = math
        # The real width, height and depth will be set during the
        # pack phase, after we know the real fontsize
        self._update_metrics()
