    def _set_aspect_ratio_correction(self):
        aspect_ratio = self.ax._get_aspect_ratio()
        if not hasattr(self._selection_artist, '_aspect_ratio_correction'):
            # Aspect ratio correction is not supported with deprecated
            # drawtype='line'. Remove this block in matplotlib 3.7
            self._aspect_ratio_correction = 1
            return

        self._selection_artist._aspect_ratio_correction = aspect_ratio
        if self._use_data_coordinates:
            self._aspect_ratio_correction = 1
        else:
            self._aspect_ratio_correction = aspect_ratio
