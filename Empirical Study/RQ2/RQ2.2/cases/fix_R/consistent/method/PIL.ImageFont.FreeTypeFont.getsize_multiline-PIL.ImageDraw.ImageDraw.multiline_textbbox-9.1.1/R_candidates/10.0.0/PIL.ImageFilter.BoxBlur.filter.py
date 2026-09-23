    def filter(self, image):
        return image.box_blur(self.radius)
