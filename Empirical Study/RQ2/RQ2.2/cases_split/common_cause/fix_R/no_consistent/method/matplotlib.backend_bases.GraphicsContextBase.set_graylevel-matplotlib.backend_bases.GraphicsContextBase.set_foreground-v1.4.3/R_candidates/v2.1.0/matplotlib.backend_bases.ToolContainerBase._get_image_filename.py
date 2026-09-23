    def _get_image_filename(self, image):
        """Find the image based on its name."""
        # TODO: better search for images, they are not always in the
        # datapath
        basedir = os.path.join(rcParams['datapath'], 'images')
        if image is not None:
            fname = os.path.join(basedir, image)
        else:
            fname = None
        return fname
