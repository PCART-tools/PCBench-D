    def _get_allsegs_and_allkinds(self):
        """
        Override in derived classes to create and return allsegs and allkinds.
        allkinds can be None.
        """
        return self.allsegs, self.allkinds
