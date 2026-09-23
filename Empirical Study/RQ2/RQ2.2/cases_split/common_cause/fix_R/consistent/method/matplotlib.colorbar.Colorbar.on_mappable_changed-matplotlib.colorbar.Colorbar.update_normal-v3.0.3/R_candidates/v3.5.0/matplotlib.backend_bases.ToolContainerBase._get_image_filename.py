    def _get_image_filename(self, image):
        """Find the image based on its name."""
        if not image:
            return None

        basedir = cbook._get_data_path("images")
        for fname in [
            image,
            image + self._icon_extension,
            str(basedir / image),
            str(basedir / (image + self._icon_extension)),
        ]:
            if os.path.isfile(fname):
                return fname
