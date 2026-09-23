    def __neg__(self):
        values = com.values_from_object(self)
        if is_bool_dtype(values):
            arr = operator.inv(values)
        elif (is_numeric_dtype(values) or is_timedelta64_dtype(values)
                or is_object_dtype(values)):
            arr = operator.neg(values)
        else:
            raise TypeError("Unary negative expects numeric dtype, not {}"
                            .format(values.dtype))
        return self.__array_wrap__(arr)
