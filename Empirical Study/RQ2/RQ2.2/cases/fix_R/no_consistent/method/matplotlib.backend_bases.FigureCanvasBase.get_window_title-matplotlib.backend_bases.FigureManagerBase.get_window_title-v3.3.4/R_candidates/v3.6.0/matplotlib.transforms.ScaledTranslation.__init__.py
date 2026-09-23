    def __init__(self, xt, yt, scale_trans, **kwargs):
        super().__init__(**kwargs)
        self._t = (xt, yt)
        self._scale_trans = scale_trans
        self.set_children(scale_trans)
        self._mtx = None
        self._inverted = None
