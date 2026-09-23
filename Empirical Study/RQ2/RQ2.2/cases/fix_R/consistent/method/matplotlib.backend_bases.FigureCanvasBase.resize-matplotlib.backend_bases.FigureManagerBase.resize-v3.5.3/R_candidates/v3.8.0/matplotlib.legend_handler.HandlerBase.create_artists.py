    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):
        """
        Return the legend artists generated.

        Parameters
        ----------
        legend : `~matplotlib.legend.Legend`
            The legend for which these legend artists are being created.
        orig_handle : `~matplotlib.artist.Artist` or similar
            The object for which these legend artists are being created.
        xdescent, ydescent, width, height : int
            The rectangle (*xdescent*, *ydescent*, *width*, *height*) that the
            legend artists being created should fit within.
        fontsize : int
            The fontsize in pixels. The legend artists being created should
            be scaled according to the given fontsize.
        trans : `~matplotlib.transforms.Transform`
            The transform that is applied to the legend artists being created.
            Typically from unit coordinates in the handler box to screen
            coordinates.
        """
        raise NotImplementedError('Derived must override')
