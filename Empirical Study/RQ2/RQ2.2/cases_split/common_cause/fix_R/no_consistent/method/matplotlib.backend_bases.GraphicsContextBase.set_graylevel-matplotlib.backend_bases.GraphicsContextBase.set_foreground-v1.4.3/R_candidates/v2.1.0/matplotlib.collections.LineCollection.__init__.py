    def __init__(self, segments,     # Can be None.
                 linewidths=None,
                 colors=None,
                 antialiaseds=None,
                 linestyles='solid',
                 offsets=None,
                 transOffset=None,
                 norm=None,
                 cmap=None,
                 pickradius=5,
                 zorder=2,
                 facecolors='none',
                 **kwargs
                 ):
        """
        *segments*
            a sequence of (*line0*, *line1*, *line2*), where::

                linen = (x0, y0), (x1, y1), ... (xm, ym)

            or the equivalent numpy array with two columns. Each line
            can be a different length.

        *colors*
            must be a sequence of RGBA tuples (e.g., arbitrary color
            strings, etc, not allowed).

        *antialiaseds*
            must be a sequence of ones or zeros

        *linestyles* [ 'solid' | 'dashed' | 'dashdot' | 'dotted' ]
            a string or dash tuple. The dash tuple is::

                (offset, onoffseq),

            where *onoffseq* is an even length tuple of on and off ink
            in points.

        If *linewidths*, *colors*, or *antialiaseds* is None, they
        default to their rcParams setting, in sequence form.

        If *offsets* and *transOffset* are not None, then
        *offsets* are transformed by *transOffset* and applied after
        the segments have been transformed to display coordinates.

        If *offsets* is not None but *transOffset* is None, then the
        *offsets* are added to the segments before any transformation.
        In this case, a single offset can be specified as::

            offsets=(xo,yo)

        and this value will be added cumulatively to each successive
        segment, so as to produce a set of successively offset curves.

        *norm*
            None (optional for :class:`matplotlib.cm.ScalarMappable`)
        *cmap*
            None (optional for :class:`matplotlib.cm.ScalarMappable`)

        *pickradius* is the tolerance for mouse clicks picking a line.
        The default is 5 pt.

        *zorder*
           The zorder of the LineCollection.  Default is 2

        *facecolors*
           The facecolors of the LineCollection. Default is 'none'
           Setting to a value other than 'none' will lead to a filled
           polygon being drawn between points on each line.

        The use of :class:`~matplotlib.cm.ScalarMappable` is optional.
        If the :class:`~matplotlib.cm.ScalarMappable` array
        :attr:`~matplotlib.cm.ScalarMappable._A` is not None (i.e., a call to
        :meth:`~matplotlib.cm.ScalarMappable.set_array` has been made), at
        draw time a call to scalar mappable will be made to set the colors.
        """
        if colors is None:
            colors = mpl.rcParams['lines.color']
        if linewidths is None:
            linewidths = (mpl.rcParams['lines.linewidth'],)
        if antialiaseds is None:
            antialiaseds = (mpl.rcParams['lines.antialiased'],)

        colors = mcolors.to_rgba_array(colors)

        Collection.__init__(
            self,
            edgecolors=colors,
            facecolors=facecolors,
            linewidths=linewidths,
            linestyles=linestyles,
            antialiaseds=antialiaseds,
            offsets=offsets,
            transOffset=transOffset,
            norm=norm,
            cmap=cmap,
            pickradius=pickradius,
            zorder=zorder,
            **kwargs)

        self.set_segments(segments)
