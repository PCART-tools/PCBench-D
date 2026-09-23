    def filter(self, image):
        xy = self.radius
        if not isinstance(xy, (tuple, list)):
            xy = (xy, xy)
        if xy == (0, 0):
            return image.copy()
        return image.box_blur(xy)
