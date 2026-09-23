    def __init__(self, transform, **kwargs):
        super().__init__(**kwargs)
        self._base_transform = transform
        self.set_children(transform)
