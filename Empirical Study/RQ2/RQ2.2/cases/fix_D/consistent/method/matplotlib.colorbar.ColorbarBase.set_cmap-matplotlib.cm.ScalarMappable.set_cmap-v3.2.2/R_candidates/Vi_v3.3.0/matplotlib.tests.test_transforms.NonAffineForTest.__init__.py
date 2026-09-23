    def __init__(self, real_trans, *args, **kwargs):
        self.real_trans = real_trans
        mtransforms.Transform.__init__(self, *args, **kwargs)
