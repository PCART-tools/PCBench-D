    def _get_repr(
        self, name=False, print_header=False, length=True, dtype=True,
            na_rep='NaN', float_format=None):
        """

        Internal function, should always return unicode string
        """

        formatter = fmt.SeriesFormatter(self, name=name, header=print_header,
                                        length=length, dtype=dtype,
                                        na_rep=na_rep,
                                        float_format=float_format)
        result = formatter.to_string()

        # TODO: following check prob. not neces.
        if not isinstance(result, compat.text_type):
            raise AssertionError("result must be of type unicode, type"
                                 " of result is {0!r}"
                                 "".format(result.__class__.__name__))
        return result
