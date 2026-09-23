    def __init__(self, left=None, bottom=None, right=None, top=None,
                 wspace=None, hspace=None):
        """
        All dimensions are fraction of the figure width or height.
        All values default to their rc params

        The following attributes are available

        left  : 0.125
            The left side of the subplots of the figure

        right : 0.9
            The right side of the subplots of the figure

        bottom : 0.1
            The bottom of the subplots of the figure

        top : 0.9
            The top of the subplots of the figure

        wspace : 0.2
            The amount of width reserved for blank space between subplots,
            expressed as a fraction of the average axis width

        hspace : 0.2
            The amount of height reserved for white space between subplots,
            expressed as a fraction of the average axis height
        """

        self.validate = True
        self.update(left, bottom, right, top, wspace, hspace)
