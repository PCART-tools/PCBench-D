    def filter(self, image: _imaging.ImagingCore) -> _imaging.ImagingCore:
        return image.unsharp_mask(self.radius, self.percent, self.threshold)
