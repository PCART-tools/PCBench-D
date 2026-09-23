    def _validate(self):
        # timedelta and integer mul/div

        if (self.is_timedelta_lhs and self.is_integer_rhs) or\
           (self.is_integer_lhs and self.is_timedelta_rhs):

            if self.name not in ('__truediv__', '__div__', '__mul__'):
                raise TypeError("can only operate on a timedelta and an "
                                "integer for division, but the operator [%s]"
                                "was passed" % self.name)

        # 2 datetimes
        elif self.is_datetime_lhs and self.is_datetime_rhs:
            if self.name != '__sub__':
                raise TypeError("can only operate on a datetimes for"
                                " subtraction, but the operator [%s] was"
                                " passed" % self.name)

        # 2 timedeltas
        elif self.is_timedelta_lhs and self.is_timedelta_rhs:

            if self.name not in ('__div__', '__truediv__', '__add__',
                                 '__sub__'):
                raise TypeError("can only operate on a timedeltas for "
                                "addition, subtraction, and division, but the"
                                " operator [%s] was passed" % self.name)

        # datetime and timedelta
        elif self.is_datetime_lhs and self.is_timedelta_rhs:

            if self.name not in ('__add__', '__sub__'):
                raise TypeError("can only operate on a datetime with a rhs of"
                                " a timedelta for addition and subtraction, "
                                " but the operator [%s] was passed" %
                                self.name)

        elif self.is_timedelta_lhs and self.is_datetime_rhs:

            if self.name != '__add__':
                raise TypeError("can only operate on a timedelta and"
                                " a datetime for addition, but the operator"
                                " [%s] was passed" % self.name)
        else:
            raise TypeError('cannot operate on a series with out a rhs '
                            'of a series/ndarray of type datetime64[ns] '
                            'or a timedelta')
