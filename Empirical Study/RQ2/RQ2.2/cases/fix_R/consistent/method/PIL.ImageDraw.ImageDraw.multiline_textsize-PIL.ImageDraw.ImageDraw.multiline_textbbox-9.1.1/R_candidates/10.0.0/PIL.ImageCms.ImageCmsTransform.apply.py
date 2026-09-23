    def apply(self, im, imOut=None):
        im.load()
        if imOut is None:
            imOut = Image.new(self.output_mode, im.size, None)
        self.transform.apply(im.im.id, imOut.im.id)
        imOut.info["icc_profile"] = self.output_profile.tobytes()
        return imOut
