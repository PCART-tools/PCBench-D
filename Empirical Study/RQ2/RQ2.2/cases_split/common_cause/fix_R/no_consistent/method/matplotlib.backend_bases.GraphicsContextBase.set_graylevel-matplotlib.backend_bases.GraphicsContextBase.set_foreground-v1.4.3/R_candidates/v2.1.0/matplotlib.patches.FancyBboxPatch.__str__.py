    def __str__(self):
        return self.__class__.__name__ \
                           + "(%g,%g;%gx%g)" % (self._x, self._y,
                                                self._width, self._height)
