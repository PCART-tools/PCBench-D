    def filter(self, image):
        if image.mode == "P":
            msg = "cannot filter palette images"
            raise ValueError(msg)
        image = image.expand(self.size // 2, self.size // 2)
        return image.rankfilter(self.size, self.rank)
