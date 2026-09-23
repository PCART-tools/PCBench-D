    def apply_in_place(self, im):
        im.load()
        if im.mode != self.output_mode:
            msg = "mode mismatch"
            raise ValueError(msg)  # wrong output mode
        self.transform.apply(im.im.id, im.im.id)
        im.info["icc_profile"] = self.output_profile.tobytes()
        return im
