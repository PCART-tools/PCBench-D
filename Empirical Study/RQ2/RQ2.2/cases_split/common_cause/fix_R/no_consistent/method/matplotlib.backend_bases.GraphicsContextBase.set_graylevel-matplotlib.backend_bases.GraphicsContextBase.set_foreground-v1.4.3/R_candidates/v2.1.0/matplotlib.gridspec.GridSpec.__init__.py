    def __init__(self, nrows, ncols,
                 left=None, bottom=None, right=None, top=None,
                 wspace=None, hspace=None,
                 width_ratios=None, height_ratios=None):
        """
        The number of rows and number of columns of the
        grid need to be set. Optionally, the subplot layout parameters
        (e.g., left, right, etc.) can be tuned.
        """
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.wspace = wspace
        self.hspace = hspace

        GridSpecBase.__init__(self, nrows, ncols,
                              width_ratios=width_ratios,
                              height_ratios=height_ratios)
