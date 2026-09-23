    def set_transform(self, trans):
        Rectangle.set_transform(self, trans)
        # the text does not get the transform!
        self.stale = True
