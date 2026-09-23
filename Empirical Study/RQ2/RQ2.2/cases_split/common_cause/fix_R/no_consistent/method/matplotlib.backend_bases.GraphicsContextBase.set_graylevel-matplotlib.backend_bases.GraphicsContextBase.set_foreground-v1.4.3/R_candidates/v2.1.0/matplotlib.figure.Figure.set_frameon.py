    def set_frameon(self, b):
        """
        Set whether the figure frame (background) is displayed or invisible

        ACCEPTS: boolean
        """
        self.frameon = b
        self.stale = True
