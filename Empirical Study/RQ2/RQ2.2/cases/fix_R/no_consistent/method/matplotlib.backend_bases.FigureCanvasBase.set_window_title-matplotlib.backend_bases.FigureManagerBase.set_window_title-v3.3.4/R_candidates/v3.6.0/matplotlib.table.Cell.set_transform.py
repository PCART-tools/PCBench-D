    def set_transform(self, trans):
        super().set_transform(trans)
        # the text does not get the transform!
        self.stale = True
