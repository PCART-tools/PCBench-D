class CapStyle(str, _AutoStringNameEnum):
    r"""
    Define how the two endpoints (caps) of an unclosed line are drawn.

    How to draw the start and end points of lines that represent a closed curve
    (i.e. that end in a `~.path.Path.CLOSEPOLY`) is controlled by the line's
    `JoinStyle`. For all other lines, how the start and end points are drawn is
    controlled by the *CapStyle*.

    For a visual impression of each *CapStyle*, `view these docs online
    <CapStyle>` or run `CapStyle.demo`.

    By default, `~.backend_bases.GraphicsContextBase` draws a stroked line as
    squared off at its endpoints.

    **Supported values:**

    .. rst-class:: value-list

        'butt'
            the line is squared off at its endpoint.
        'projecting'
            the line is squared off as in *butt*, but the filled in area
            extends beyond the endpoint a distance of ``linewidth/2``.
        'round'
            like *butt*, but a semicircular cap is added to the end of the
            line, of radius ``linewidth/2``.

    .. plot::
        :alt: Demo of possible CapStyle's

        from matplotlib._enums import CapStyle
        CapStyle.demo()

    """
    butt = auto()
    projecting = auto()
    round = auto()

    @staticmethod
    def demo():
        """Demonstrate how each CapStyle looks for a thick line segment."""
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(4, 1.2))
        ax = fig.add_axes([0, 0, 1, 0.8])
        ax.set_title('Cap style')

        for x, style in enumerate(['butt', 'round', 'projecting']):
            ax.text(x+0.25, 0.85, style, ha='center')
            xx = [x, x+0.5]
            yy = [0, 0]
            ax.plot(xx, yy, lw=12, color='tab:blue', solid_capstyle=style)
            ax.plot(xx, yy, lw=1, color='black')
            ax.plot(xx, yy, 'o', color='tab:red', markersize=3)

        ax.set_ylim(-.5, 1.5)
        ax.set_axis_off()
        fig.show()
