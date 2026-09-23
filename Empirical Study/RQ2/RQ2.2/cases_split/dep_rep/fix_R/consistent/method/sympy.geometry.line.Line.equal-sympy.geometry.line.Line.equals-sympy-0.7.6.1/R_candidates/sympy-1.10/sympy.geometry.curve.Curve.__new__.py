    def __new__(cls, function, limits):
        fun = sympify(function)
        if not is_sequence(fun) or len(fun) != 2:
            raise ValueError("Function argument should be (x(t), y(t)) "
                "but got %s" % str(function))
        if not is_sequence(limits) or len(limits) != 3:
            raise ValueError("Limit argument should be (t, tmin, tmax) "
                "but got %s" % str(limits))

        return GeometryEntity.__new__(cls, Tuple(*fun), Tuple(*limits))
