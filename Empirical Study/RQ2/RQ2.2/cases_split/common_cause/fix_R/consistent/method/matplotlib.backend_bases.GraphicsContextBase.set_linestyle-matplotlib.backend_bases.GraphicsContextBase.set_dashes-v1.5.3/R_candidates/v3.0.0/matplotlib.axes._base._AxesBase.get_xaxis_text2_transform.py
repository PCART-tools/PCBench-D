    def get_xaxis_text2_transform(self, pad_points):
        """
        Get the transformation used for drawing the secondary x-axis
        labels, which will add the given amount of padding (in points)
        between the axes and the label.  The x-direction is in data
        coordinates and the y-direction is in axis coordinates.
        Returns a 3-tuple of the form::

          (transform, valign, halign)

        where *valign* and *halign* are requested alignments for the
        text.

        .. note::

            This transformation is primarily used by the
            :class:`~matplotlib.axis.Axis` class, and is meant to be
            overridden by new kinds of projections that may need to
            place axis elements in different locations.

        """
        labels_align = matplotlib.rcParams["xtick.alignment"]
        return (self.get_xaxis_transform(which='tick2') +
                mtransforms.ScaledTranslation(0, pad_points / 72,
                                              self.figure.dpi_scale_trans),
                "bottom", labels_align)
