    def _set_device_pixel_ratio(self, ratio):
        # Cairo in GTK4 always uses logical pixels, so we don't need to do anything for
        # changes to the device pixel ratio.
        return False
