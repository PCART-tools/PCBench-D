    def filter(self, image: _imaging.ImagingCore) -> _imaging.ImagingCore:
        return image.modefilter(self.size)
