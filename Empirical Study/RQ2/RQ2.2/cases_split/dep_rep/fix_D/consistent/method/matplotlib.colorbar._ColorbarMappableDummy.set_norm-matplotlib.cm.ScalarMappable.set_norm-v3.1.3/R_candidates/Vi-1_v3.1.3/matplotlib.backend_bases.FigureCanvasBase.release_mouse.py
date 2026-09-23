    def release_mouse(self, ax):
        """
        Release the mouse grab held by the axes, ax.
        Usually called by the widgets.
        It is ok to call this even if you ax doesn't have the mouse
        grab currently.
        """
        if self.mouse_grabber is ax:
            self.mouse_grabber = None
