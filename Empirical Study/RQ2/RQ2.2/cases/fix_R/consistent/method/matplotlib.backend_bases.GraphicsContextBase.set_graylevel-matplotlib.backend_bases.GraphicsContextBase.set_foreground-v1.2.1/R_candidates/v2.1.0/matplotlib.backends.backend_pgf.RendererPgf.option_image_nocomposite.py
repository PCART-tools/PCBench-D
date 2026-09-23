    def option_image_nocomposite(self):
        """
        return whether to generate a composite image from multiple images on
        a set of axes
        """
        return not rcParams['image.composite_image']
