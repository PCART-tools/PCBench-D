    def get_yaxis_text1_transform(self, pad_points):
        """
        Get the transformation used for drawing y-axis labels, which
        will add the given amount of padding (in points) between the
        axes and the label.  The x-direction is in axis coordinates
        and the y-direction is in data coordinates.  Returns a 3-tuple
        of the form::

          (transform, valign, halign)

        where *valign* and *halign* are requested alignments for the
        text.

        .. note::

            This transformation is primarily used by the
            :class:`~matplotlib.axis.Axis` class, and is meant to be
            overridden by new kinds of projections that may need to
            place axis elements in different locations.

        """
        labels_align = matplotlib.rcParams["ytick.alignment"]
        return (self.get_yaxis_transform(which='tick1') +
                mtransforms.ScaledTranslation(-1 * pad_points / 72.0, 0,
                                              self.figure.dpi_scale_trans),
                labels_align, "right")
