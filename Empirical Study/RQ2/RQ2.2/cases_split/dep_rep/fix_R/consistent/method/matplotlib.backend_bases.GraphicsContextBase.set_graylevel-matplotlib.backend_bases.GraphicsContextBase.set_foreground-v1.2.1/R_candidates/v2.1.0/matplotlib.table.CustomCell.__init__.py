    def __init__(self, *args, **kwargs):
        visible_edges = kwargs.pop('visible_edges')
        Cell.__init__(self, *args, **kwargs)
        self.visible_edges = visible_edges
