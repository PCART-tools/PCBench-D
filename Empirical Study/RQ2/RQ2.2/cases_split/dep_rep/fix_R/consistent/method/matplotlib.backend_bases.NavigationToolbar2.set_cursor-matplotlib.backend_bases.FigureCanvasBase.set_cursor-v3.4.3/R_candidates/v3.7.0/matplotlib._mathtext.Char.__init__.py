    def __init__(self, c, state):
        super().__init__()
        self.c = c
        self.fontset = state.fontset
        self.font = state.font
        self.font_class = state.font_class
        self.fontsize = state.fontsize
        self.dpi = state.dpi
        # The real width, height and depth will be set during the
        # pack phase, after we know the real fontsize
        self._update_metrics()
