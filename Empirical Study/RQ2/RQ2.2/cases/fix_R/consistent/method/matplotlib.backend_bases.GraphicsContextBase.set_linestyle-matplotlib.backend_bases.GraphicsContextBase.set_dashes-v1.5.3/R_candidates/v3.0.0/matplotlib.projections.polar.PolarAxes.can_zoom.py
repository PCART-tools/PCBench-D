    def can_zoom(self):
        """
        Return *True* if this axes supports the zoom box button functionality.

        Polar axes do not support zoom boxes.
        """
        return False
