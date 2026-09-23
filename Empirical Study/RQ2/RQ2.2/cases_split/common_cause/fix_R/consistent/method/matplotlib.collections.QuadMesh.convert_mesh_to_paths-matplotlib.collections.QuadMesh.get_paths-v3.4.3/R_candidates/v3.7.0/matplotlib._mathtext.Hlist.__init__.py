    def __init__(self, elements, w=0., m='additional', do_kern=True):
        super().__init__(elements)
        if do_kern:
            self.kern()
        self.hpack(w=w, m=m)
