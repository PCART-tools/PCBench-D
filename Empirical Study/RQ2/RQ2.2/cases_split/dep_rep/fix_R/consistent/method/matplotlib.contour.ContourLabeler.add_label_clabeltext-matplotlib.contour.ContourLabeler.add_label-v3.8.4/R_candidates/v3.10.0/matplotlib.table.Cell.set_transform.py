    def set_transform(self, t):
        super().set_transform(t)
        # the text does not get the transform!
        self.stale = True
