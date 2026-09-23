    def load(self):
        if not self.fp:
            self.fp = self.ole.openstream(self.stream[:2] + ["Subimage 0000 Data"])

        return ImageFile.ImageFile.load(self)
