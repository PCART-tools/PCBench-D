    def _get_image_filename(self, image):
        """Find the image based on its name."""
        if not image:
            return None

        basedir = os.path.join(rcParams['datapath'], 'images')
        possible_images = (
            image,
            image + self._icon_extension,
            os.path.join(basedir, image),
            os.path.join(basedir, image) + self._icon_extension)

        for fname in possible_images:
            if os.path.isfile(fname):
                return fname
