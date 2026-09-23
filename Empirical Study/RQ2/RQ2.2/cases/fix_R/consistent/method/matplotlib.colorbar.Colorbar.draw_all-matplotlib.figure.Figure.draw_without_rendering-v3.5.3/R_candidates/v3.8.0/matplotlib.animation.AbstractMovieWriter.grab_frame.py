    @abc.abstractmethod
    def grab_frame(self, **savefig_kwargs):
        """
        Grab the image information from the figure and save as a movie frame.

        All keyword arguments in *savefig_kwargs* are passed on to the
        `~.Figure.savefig` call that saves the figure.  However, several
        keyword arguments that are supported by `~.Figure.savefig` may not be
        passed as they are controlled by the MovieWriter:

        - *dpi*, *bbox_inches*:  These may not be passed because each frame of the
           animation much be exactly the same size in pixels.
        - *format*: This is controlled by the MovieWriter.
        """
