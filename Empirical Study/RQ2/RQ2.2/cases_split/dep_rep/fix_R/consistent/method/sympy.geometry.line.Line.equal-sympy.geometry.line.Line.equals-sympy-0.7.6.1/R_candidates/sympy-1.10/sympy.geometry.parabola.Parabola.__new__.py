    def __new__(cls, focus=None, directrix=None, **kwargs):

        if focus:
            focus = Point(focus, dim=2)
        else:
            focus = Point(0, 0)

        directrix = Line(directrix)

        if (directrix.slope != 0 and directrix.slope != S.Infinity):
            raise NotImplementedError('The directrix must be a horizontal'
                                      ' or vertical line')
        if directrix.contains(focus):
            raise ValueError('The focus must not be a point of directrix')

        return GeometryEntity.__new__(cls, focus, directrix, **kwargs)
