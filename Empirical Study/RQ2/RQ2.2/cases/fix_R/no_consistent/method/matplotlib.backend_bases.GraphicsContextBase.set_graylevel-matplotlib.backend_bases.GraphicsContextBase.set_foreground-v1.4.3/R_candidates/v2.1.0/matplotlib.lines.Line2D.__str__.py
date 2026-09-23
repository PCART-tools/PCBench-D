    def __str__(self):
        if self._label != "":
            return "Line2D(%s)" % (self._label)
        elif self._x is None:
            return "Line2D()"
        elif len(self._x) > 3:
            return "Line2D((%g,%g),(%g,%g),...,(%g,%g))"\
                % (self._x[0], self._y[0], self._x[0],
                   self._y[0], self._x[-1], self._y[-1])
        else:
            return "Line2D(%s)"\
                % (",".join(["(%g,%g)" % (x, y) for x, y
                             in zip(self._x, self._y)]))
