    def create_dummy_axis(self, **kwargs):
        if self.axis is None:
            self.axis = _DummyAxis(**kwargs)
