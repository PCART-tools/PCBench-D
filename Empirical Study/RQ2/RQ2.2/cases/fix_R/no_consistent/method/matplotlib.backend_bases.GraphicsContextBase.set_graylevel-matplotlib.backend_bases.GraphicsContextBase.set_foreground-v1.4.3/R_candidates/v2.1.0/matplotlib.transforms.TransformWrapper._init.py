    def _init(self, child):
        Transform.__init__(self)
        self.input_dims = child.input_dims
        self.output_dims = child.output_dims
        self._set(child)
        self._invalid = 0
