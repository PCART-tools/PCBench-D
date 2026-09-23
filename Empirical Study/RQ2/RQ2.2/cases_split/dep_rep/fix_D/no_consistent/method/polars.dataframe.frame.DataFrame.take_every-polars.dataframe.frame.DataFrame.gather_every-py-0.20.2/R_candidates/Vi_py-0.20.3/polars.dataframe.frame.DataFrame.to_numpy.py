    @deprecate_nonkeyword_arguments(version="0.19.3")
    def to_numpy(
        self,
        structured: bool = False,  # noqa: FBT001
        *,
        order: IndexOrder = "fortran",
        use_pyarrow: bool = True,
    ) -> np.ndarray[Any, Any]:
        """
        Convert DataFrame to a 2D NumPy array.

        This operation clones data.

        Parameters
        ----------
        structured
            Optionally return a structured array, with field names and
            dtypes that correspond to the DataFrame schema.
        order
            The index order of the returned NumPy array, either C-like or
            Fortran-like. In general, using the Fortran-like index order is faster.
            However, the C-like order might be more appropriate to use for downstream
            applications to prevent cloning data, e.g. when reshaping into a
            one-dimensional array. Note that this option only takes effect if
            `structured` is set to `False` and the DataFrame dtypes allow for a
            global dtype for all columns.
        use_pyarrow
            Use `pyarrow.Array.to_numpy
            <https://arrow.apache.org/docs/python/generated/pyarrow.Array.html#pyarrow.Array.to_numpy>`_

            function for the conversion to numpy if necessary.

        Notes
        -----
        If you're attempting to convert String or Decimal to an array, you'll need to
        install `pyarrow`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.5, 7.0, 8.5],
        ...         "ham": ["a", "b", "c"],
        ...     },
        ...     schema_overrides={"foo": pl.UInt8, "bar": pl.Float32},
        ... )

        Export to a standard 2D numpy array.

        >>> df.to_numpy()
        array([[1, 6.5, 'a'],
               [2, 7.0, 'b'],
               [3, 8.5, 'c']], dtype=object)

        Export to a structured array, which can better-preserve individual
        column data, such as name and dtype...

        >>> df.to_numpy(structured=True)
        array([(1, 6.5, 'a'), (2, 7. , 'b'), (3, 8.5, 'c')],
              dtype=[('foo', 'u1'), ('bar', '<f4'), ('ham', '<U1')])

        ...optionally going on to view as a record array:

        >>> import numpy as np
        >>> df.to_numpy(structured=True).view(np.recarray)
        rec.array([(1, 6.5, 'a'), (2, 7. , 'b'), (3, 8.5, 'c')],
                  dtype=[('foo', 'u1'), ('bar', '<f4'), ('ham', '<U1')])

        """
        if structured:
            # see: https://numpy.org/doc/stable/user/basics.rec.html
            arrays = []
            for c, tp in self.schema.items():
                s = self[c]
                a = s.to_numpy(use_pyarrow=use_pyarrow)
                arrays.append(
                    a.astype(str, copy=False)
                    if tp == String and not s.null_count()
                    else a
                )

            out = np.empty(
                len(self), dtype=list(zip(self.columns, (a.dtype for a in arrays)))
            )
            for idx, c in enumerate(self.columns):
                out[c] = arrays[idx]
        else:
            out = self._df.to_numpy(order)
            if out is None:
                return np.vstack(
                    [
                        self.to_series(i).to_numpy(use_pyarrow=use_pyarrow)
                        for i in range(self.width)
                    ]
                ).T

        return out
