    def to_string(self, buf=None, na_rep='NaN', float_format=None, header=True,
                  index=True, length=False, dtype=False, name=False,
                  max_rows=None):
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
        header: boolean, default True
            Add the Series header (index name)
        index : bool, optional
            Add index (row) labels, default True
        length : boolean, default False
            Add the Series length
        dtype : boolean, default False
            Add the Series dtype
        name : boolean, default False
            Add the Series name if not None
        max_rows : int, optional
            Maximum number of rows to show before truncating. If None, show
            all.

        Returns
        -------
        formatted : string (if not buffer passed)
        """

        formatter = fmt.SeriesFormatter(self, name=name, length=length,
                                        header=header, index=index,
                                        dtype=dtype, na_rep=na_rep,
                                        float_format=float_format,
                                        max_rows=max_rows)
        result = formatter.to_string()

        # catch contract violations
        if not isinstance(result, compat.text_type):
            raise AssertionError("result must be of type unicode, type"
                                 " of result is {0!r}"
                                 "".format(result.__class__.__name__))

        if buf is None:
            return result
        else:
            try:
                buf.write(result)
            except AttributeError:
                with open(buf, 'w') as f:
                    f.write(result)
