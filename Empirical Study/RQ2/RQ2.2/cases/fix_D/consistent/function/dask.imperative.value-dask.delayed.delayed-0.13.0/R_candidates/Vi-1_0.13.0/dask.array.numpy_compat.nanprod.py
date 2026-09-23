    def nanprod(a, axis=None, dtype=None, out=None, keepdims=0):
        """
        Return the product of array elements over a given axis treating Not a
        Numbers (NaNs) as zero.

        One is returned for slices that are all-NaN or empty.

        .. versionadded:: 1.10.0

        Parameters
        ----------
        a : array_like
            Array containing numbers whose sum is desired. If `a` is not an
            array, a conversion is attempted.
        axis : int, optional
            Axis along which the product is computed. The default is to compute
            the product of the flattened array.
        dtype : data-type, optional
            The type of the returned array and of the accumulator in which the
            elements are summed.  By default, the dtype of `a` is used.  An
            exception is when `a` has an integer type with less precision than
            the platform (u)intp. In that case, the default will be either
            (u)int32 or (u)int64 depending on whether the platform is 32 or 64
            bits. For inexact inputs, dtype must be inexact.
        out : ndarray, optional
            Alternate output array in which to place the result.  The default
            is ``None``. If provided, it must have the same shape as the
            expected output, but the type will be cast if necessary.  See
            `doc.ufuncs` for details. The casting of NaN to integer can yield
            unexpected results.
        keepdims : bool, optional
            If True, the axes which are reduced are left in the result as
            dimensions with size one. With this option, the result will
            broadcast correctly against the original `arr`.

        Returns
        -------
        y : ndarray or numpy scalar

        See Also
        --------
        numpy.prod : Product across array propagating NaNs.
        isnan : Show which elements are NaN.

        Notes
        -----
        Numpy integer arithmetic is modular. If the size of a product exceeds
        the size of an integer accumulator, its value will wrap around and the
        result will be incorrect. Specifying ``dtype=double`` can alleviate
        that problem.

        Examples
        --------
        >>> np.nanprod(1)
        1
        >>> np.nanprod([1])
        1
        >>> np.nanprod([1, np.nan])
        1.0
        >>> a = np.array([[1, 2], [3, np.nan]])
        >>> np.nanprod(a)
        6.0
        >>> np.nanprod(a, axis=0)
        array([ 3.,  2.])

        """
        a, mask = _replace_nan(a, 1)
        return np.prod(a, axis=axis, dtype=dtype, out=out, keepdims=keepdims)
