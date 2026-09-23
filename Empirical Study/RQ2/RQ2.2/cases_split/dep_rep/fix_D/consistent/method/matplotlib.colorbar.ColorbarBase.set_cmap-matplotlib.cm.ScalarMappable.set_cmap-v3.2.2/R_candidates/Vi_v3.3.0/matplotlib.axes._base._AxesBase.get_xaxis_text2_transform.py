    def get_xaxis_text2_transform(self, pad_points):
        """
        Returns
        -------
        transform : Transform
            The transform used for drawing secondary x-axis labels, which will
            add *pad_points* of padding (in points) between the axes and the
            label.  The x-direction is in data coordinates and the y-direction
            is in axis corrdinates
        valign : {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
            The text vertical alignment.
        halign : {'center', 'left', 'right'}
            The text horizontal alignment.

        Notes
        -----
        This transformation is primarily used by the `~matplotlib.axis.Axis`
        class, and is meant to be overridden by new kinds of projections that
        may need to place axis elements in different locations.
        """
        labels_align = mpl.rcParams["xtick.alignment"]
        return (self.get_xaxis_transform(which='tick2') +
                mtransforms.ScaledTranslation(0, pad_points / 72,
                                              self.figure.dpi_scale_trans),
                "bottom", labels_align)
