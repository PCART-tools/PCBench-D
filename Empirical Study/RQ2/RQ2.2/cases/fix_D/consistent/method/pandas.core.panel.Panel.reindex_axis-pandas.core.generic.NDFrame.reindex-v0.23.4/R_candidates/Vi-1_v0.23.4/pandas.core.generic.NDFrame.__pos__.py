    def __pos__(self):
        values = com._values_from_object(self)
        if (is_bool_dtype(values) or is_period_arraylike(values)):
            arr = values
        elif (is_numeric_dtype(values) or is_timedelta64_dtype(values)
                or is_object_dtype(values)):
            arr = operator.pos(values)
        else:
            raise TypeError("Unary plus expects numeric dtype, not {}"
                            .format(values.dtype))
        return self.__array_wrap__(arr)
