    def filter(self, image: _imaging.ImagingCore) -> _imaging.ImagingCore:
        from . import Image

        return image.color_lut_3d(
            self.mode or image.mode,
            Image.Resampling.BILINEAR,
            self.channels,
            self.size[0],
            self.size[1],
            self.size[2],
            self.table,
        )
