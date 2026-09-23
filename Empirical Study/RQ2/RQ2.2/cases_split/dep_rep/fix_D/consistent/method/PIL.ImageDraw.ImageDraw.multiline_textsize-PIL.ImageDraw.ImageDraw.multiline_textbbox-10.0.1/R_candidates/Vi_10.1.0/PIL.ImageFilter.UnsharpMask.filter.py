    def filter(self, image):
        return image.unsharp_mask(self.radius, self.percent, self.threshold)
