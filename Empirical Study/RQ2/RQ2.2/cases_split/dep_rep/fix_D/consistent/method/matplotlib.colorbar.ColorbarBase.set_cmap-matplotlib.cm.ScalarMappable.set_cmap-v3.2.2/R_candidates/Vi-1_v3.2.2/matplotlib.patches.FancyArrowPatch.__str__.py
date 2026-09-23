    def __str__(self):

        if self._posA_posB is not None:
            (x1, y1), (x2, y2) = self._posA_posB
            return self.__class__.__name__ \
                + "((%g, %g)->(%g, %g))" % (x1, y1, x2, y2)
        else:
            return self.__class__.__name__ \
                + "(%s)" % (str(self._path_original),)
