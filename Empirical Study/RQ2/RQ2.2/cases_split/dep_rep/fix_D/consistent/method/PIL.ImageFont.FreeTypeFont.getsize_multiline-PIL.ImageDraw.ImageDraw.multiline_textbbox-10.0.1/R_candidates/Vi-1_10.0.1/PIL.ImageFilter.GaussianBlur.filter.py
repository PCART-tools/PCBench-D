    def filter(self, image):
        return image.gaussian_blur(self.radius)
