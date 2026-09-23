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
        Parameters
        ----------
        segments: list of array-like
            A sequence of (*line0*, *line1*, *line2*), where::

                linen = (x0, y0), (x1, y1), ... (xm, ym)

            or the equivalent numpy array with two columns. Each line
            can have a different number of segments.
        linewidths : float or list of float, default: :rc:`lines.linewidth`
            The width of each line in points.
        colors : color or list of color, default: :rc:`lines.color`
            A sequence of RGBA tuples (e.g., arbitrary color strings, etc, not
            allowed).
        antialiaseds : bool or list of bool, default: :rc:`lines.antialiased`
            Whether to use antialiasing for each line.
        zorder : int, default: 2
           zorder of the lines once drawn.
        facecolors : color or list of color, default: 'none'
           The facecolors of the LineCollection.
           Setting to a value other than 'none' will lead to each line being
           "filled in" as if there was an implicit line segment joining the
           last and first points of that line back around to each other. In
           order to manually specify what should count as the "interior" of
           each line, please use `.PathCollection` instead, where the
           "interior" can be specified by appropriate usage of
           `~.path.Path.CLOSEPOLY`.
        **kwargs
            Forwareded to `.Collection`.
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
            zorder=zorder,
            **kwargs)

        self.set_segments(segments)
