    def to_string(self, buf=None, na_rep='NaN', float_format=None,
                  nanRep=None, length=False, dtype=False, name=False):
        """
        Render a string representation of the Series

        Parameters
        ----------
        buf : StringIO-like, optional
            buffer to write to
        na_rep : string, optional
            string representation of NAN to use, default 'NaN'
        float_format : one-parameter function, optional
            formatter function to apply to columns' elements if they are floats
            default None
        length : boolean, default False
            Add the Series length
        dtype : boolean, default False
            Add the Series dtype
        name : boolean, default False
            Add the Series name (which may be None)

        Returns
        -------
        formatted : string (if not buffer passed)
        """

        if nanRep is not None:  # pragma: no cover
            warnings.warn("nanRep is deprecated, use na_rep", FutureWarning)
            na_rep = nanRep

        the_repr = self._get_repr(float_format=float_format, na_rep=na_rep,
                                  length=length, dtype=dtype, name=name)

        # catch contract violations
        if not isinstance(the_repr, compat.text_type):
            raise AssertionError("result must be of type unicode, type"
                                 " of result is {0!r}"
                                 "".format(the_repr.__class__.__name__))

        if buf is None:
            return the_repr
        else:
            try:
                buf.write(the_repr)
            except AttributeError:
                with open(buf, 'w') as f:
                    f.write(the_repr)
