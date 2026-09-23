    def apply(self, im: Image.Image, imOut: Image.Image | None = None) -> Image.Image:
        if imOut is None:
            imOut = Image.new(self.output_mode, im.size, None)
        self.transform.apply(im.getim(), imOut.getim())
        imOut.info["icc_profile"] = self.output_profile.tobytes()
        return imOut
