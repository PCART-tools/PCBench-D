    def _validate(self, lvalues, rvalues, name):
        # timedelta and integer mul/div

        if ((self.is_timedelta_lhs and
                (self.is_integer_rhs or self.is_floating_rhs)) or
            (self.is_timedelta_rhs and
                (self.is_integer_lhs or self.is_floating_lhs))):

            if name not in ('__div__', '__truediv__', '__mul__', '__rmul__'):
                raise TypeError("can only operate on a timedelta and an "
                                "integer or a float for division and "
                                "multiplication, but the operator [{name}] "
                                "was passed".format(name=name))

        # 2 timedeltas
        elif ((self.is_timedelta_lhs and
               (self.is_timedelta_rhs or self.is_offset_rhs)) or
              (self.is_timedelta_rhs and
               (self.is_timedelta_lhs or self.is_offset_lhs))):

            if name not in ('__div__', '__rdiv__', '__truediv__',
                            '__rtruediv__', '__add__', '__radd__', '__sub__',
                            '__rsub__'):
                raise TypeError("can only operate on a timedeltas for addition"
                                ", subtraction, and division, but the operator"
                                " [{name}] was passed".format(name=name))

        # datetime and timedelta/DateOffset
        elif (self.is_datetime_lhs and
              (self.is_timedelta_rhs or self.is_offset_rhs)):

            if name not in ('__add__', '__radd__', '__sub__'):
                raise TypeError("can only operate on a datetime with a rhs of "
                                "a timedelta/DateOffset for addition and "
                                "subtraction, but the operator [{name}] was "
                                "passed".format(name=name))

        elif (self.is_datetime_rhs and
              (self.is_timedelta_lhs or self.is_offset_lhs)):
            if name not in ('__add__', '__radd__', '__rsub__'):
                raise TypeError("can only operate on a timedelta/DateOffset "
                                "with a rhs of a datetime for addition, "
                                "but the operator [{name}] was passed"
                                .format(name=name))

        # 2 datetimes
        elif self.is_datetime_lhs and self.is_datetime_rhs:

            if name not in ('__sub__', '__rsub__'):
                raise TypeError("can only operate on a datetimes for"
                                " subtraction, but the operator [{name}] was"
                                " passed".format(name=name))

            # if tz's must be equal (same or None)
            if getattr(lvalues, 'tz', None) != getattr(rvalues, 'tz', None):
                raise ValueError("Incompatible tz's on datetime subtraction "
                                 "ops")

        elif ((self.is_timedelta_lhs or self.is_offset_lhs) and
              self.is_datetime_rhs):

            if name not in ('__add__', '__radd__'):
                raise TypeError("can only operate on a timedelta/DateOffset "
                                "and a datetime for addition, but the operator"
                                " [{name}] was passed".format(name=name))
        else:
            raise TypeError('cannot operate on a series without a rhs '
                            'of a series/ndarray of type datetime64[ns] '
                            'or a timedelta')
