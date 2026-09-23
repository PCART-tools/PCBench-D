    @docstring.dedent_interpd
    def __init__(self, xy, width, height, angle=0.0,
                 theta1=0.0, theta2=360.0, **kwargs):
        """
        The following args are supported:

        *xy*
          center of ellipse

        *width*
          length of horizontal axis

        *height*
          length of vertical axis

        *angle*
          rotation in degrees (anti-clockwise)

        *theta1*
          starting angle of the arc in degrees

        *theta2*
          ending angle of the arc in degrees

        If *theta1* and *theta2* are not provided, the arc will form a
        complete ellipse.

        Valid kwargs are:

        %(Patch)s
        """
        fill = kwargs.setdefault('fill', False)
        if fill:
            raise ValueError("Arc objects can not be filled")

        Ellipse.__init__(self, xy, width, height, angle, **kwargs)

        self.theta1 = theta1
        self.theta2 = theta2
