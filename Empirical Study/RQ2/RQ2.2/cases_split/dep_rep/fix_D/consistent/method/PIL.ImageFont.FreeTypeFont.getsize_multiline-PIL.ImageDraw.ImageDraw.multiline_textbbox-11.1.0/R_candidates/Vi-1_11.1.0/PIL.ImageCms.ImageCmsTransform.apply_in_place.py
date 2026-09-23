    def apply_in_place(self, im: Image.Image) -> Image.Image:
        if im.mode != self.output_mode:
            msg = "mode mismatch"
            raise ValueError(msg)  # wrong output mode
        self.transform.apply(im.getim(), im.getim())
        im.info["icc_profile"] = self.output_profile.tobytes()
        return im
