    def __init__(self, transform, **kwargs):
        super().__init__(**kwargs)
        self._base_transform = transform
