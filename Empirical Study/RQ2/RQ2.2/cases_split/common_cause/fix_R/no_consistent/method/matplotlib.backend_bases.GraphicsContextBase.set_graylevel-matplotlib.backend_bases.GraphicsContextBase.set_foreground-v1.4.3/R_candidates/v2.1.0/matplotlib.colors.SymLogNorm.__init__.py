    def __init__(self,  linthresh, linscale=1.0,
                 vmin=None, vmax=None, clip=False):
        """
        *linthresh*:
        The range within which the plot is linear (to
        avoid having the plot go to infinity around zero).

        *linscale*:
        This allows the linear range (-*linthresh* to *linthresh*)
        to be stretched relative to the logarithmic range.  Its
        value is the number of decades to use for each half of the
        linear range.  For example, when *linscale* == 1.0 (the
        default), the space used for the positive and negative
        halves of the linear range will be equal to one decade in
        the logarithmic range. Defaults to 1.
        """
        Normalize.__init__(self, vmin, vmax, clip)
        self.linthresh = float(linthresh)
        self._linscale_adj = (linscale / (1.0 - np.e ** -1))
        if vmin is not None and vmax is not None:
            self._transform_vmin_vmax()
