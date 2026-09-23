    def option_image_nocomposite(self):
        """
        override this method for renderers that do not necessarily always
        want to rescale and composite raster images. (like SVG, PDF, or PS)
        """
        return False
