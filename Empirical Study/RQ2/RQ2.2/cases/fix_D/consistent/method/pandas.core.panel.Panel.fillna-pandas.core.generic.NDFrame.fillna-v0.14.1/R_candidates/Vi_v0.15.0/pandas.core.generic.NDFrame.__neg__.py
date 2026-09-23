    def __neg__(self):
        values = _values_from_object(self)
        if values.dtype == np.bool_:
            arr = operator.inv(values)
        else:
            arr = operator.neg(values)
        return self.__array_wrap__(arr)
