    def get_images(self):
        """return a list of Axes images contained by the Axes"""
        return cbook.silent_list('AxesImage', self.images)
