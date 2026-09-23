    def _rgb(self, rgba):
        h, w = rgba.shape[:2]
        rgb = rgba[::-1, :, :3]
        return h, w, rgb.tostring()
