    def _repr_svg_(self):
        """SVG representation of a GeometryEntity suitable for IPython"""

        try:
            bounds = self.bounds
        except (NotImplementedError, TypeError):
            # if we have no SVG representation, return None so IPython
            # will fall back to the next representation
            return None

        if not all(x.is_number and x.is_finite for x in bounds):
            return None

        svg_top = '''<svg xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            width="{1}" height="{2}" viewBox="{0}"
            preserveAspectRatio="xMinYMin meet">
            <defs>
                <marker id="markerCircle" markerWidth="8" markerHeight="8"
                    refx="5" refy="5" markerUnits="strokeWidth">
                    <circle cx="5" cy="5" r="1.5" style="stroke: none; fill:#000000;"/>
                </marker>
                <marker id="markerArrow" markerWidth="13" markerHeight="13" refx="2" refy="4"
                       orient="auto" markerUnits="strokeWidth">
                    <path d="M2,2 L2,6 L6,4" style="fill: #000000;" />
                </marker>
                <marker id="markerReverseArrow" markerWidth="13" markerHeight="13" refx="6" refy="4"
                       orient="auto" markerUnits="strokeWidth">
                    <path d="M6,2 L6,6 L2,4" style="fill: #000000;" />
                </marker>
            </defs>'''

        # Establish SVG canvas that will fit all the data + small space
        xmin, ymin, xmax, ymax = map(N, bounds)
        if xmin == xmax and ymin == ymax:
            # This is a point; buffer using an arbitrary size
            xmin, ymin, xmax, ymax = xmin - .5, ymin -.5, xmax + .5, ymax + .5
        else:
            # Expand bounds by a fraction of the data ranges
            expand = 0.1  # or 10%; this keeps arrowheads in view (R plots use 4%)
            widest_part = max([xmax - xmin, ymax - ymin])
            expand_amount = widest_part * expand
            xmin -= expand_amount
            ymin -= expand_amount
            xmax += expand_amount
            ymax += expand_amount
        dx = xmax - xmin
        dy = ymax - ymin
        width = min([max([100., dx]), 300])
        height = min([max([100., dy]), 300])

        scale_factor = 1. if max(width, height) == 0 else max(dx, dy) / max(width, height)
        try:
            svg = self._svg(scale_factor)
        except (NotImplementedError, TypeError):
            # if we have no SVG representation, return None so IPython
            # will fall back to the next representation
            return None

        view_box = "{} {} {} {}".format(xmin, ymin, dx, dy)
        transform = "matrix(1,0,0,-1,0,{})".format(ymax + ymin)
        svg_top = svg_top.format(view_box, width, height)

        return svg_top + (
            '<g transform="{}">{}</g></svg>'
            ).format(transform, svg)
