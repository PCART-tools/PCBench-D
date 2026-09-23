class Array(DaskMethodsMixin):
    """ Parallel Dask Array

    A parallel nd-array comprised of many numpy arrays arranged in a grid.

    This constructor is for advanced uses only.  For normal use see the
    ``da.from_array`` function.

    Parameters
    ----------

    dask : dict
        Task dependency graph
    name : string
        Name of array in dask
    shape : tuple of ints
        Shape of the entire array
    chunks: iterable of tuples
        block sizes along each dimension

    See Also
    --------
    dask.array.from_array
    """
    __slots__ = 'dask', '_name', '_cached_keys', '_chunks', 'dtype'

    def __new__(cls, dask, name, chunks, dtype, shape=None):
        self = super(Array, cls).__new__(cls)
        assert isinstance(dask, Mapping)
        if not isinstance(dask, ShareDict):
            s = ShareDict()
            s.update_with_key(dask, key=name)
            dask = s
        self.dask = dask
        self.name = name
        if dtype is None:
            raise ValueError("You must specify the dtype of the array")
        self.dtype = np.dtype(dtype)

        self._chunks = normalize_chunks(chunks, shape, dtype=self.dtype)
        if self._chunks is None:
            raise ValueError(CHUNKS_NONE_ERROR_MESSAGE)

        for plugin in config.get('array_plugins', ()):
            result = plugin(self)
            if result is not None:
                self = result

        return self

    def __reduce__(self):
        return (Array, (self.dask, self.name, self.chunks, self.dtype))

    def __dask_graph__(self):
        return self.dask

    def __dask_keys__(self):
        if self._cached_keys is not None:
            return self._cached_keys

        name, chunks, numblocks = self.name, self.chunks, self.numblocks

        def keys(*args):
            if not chunks:
                return [(name,)]
            ind = len(args)
            if ind + 1 == len(numblocks):
                result = [(name,) + args + (i,) for i in range(numblocks[ind])]
            else:
                result = [keys(*(args + (i,))) for i in range(numblocks[ind])]
            return result

        self._cached_keys = result = keys()
        return result

    def __dask_tokenize__(self):
        return self.name

    __dask_optimize__ = globalmethod(optimize, key='array_optimize',
                                     falsey=dont_optimize)
    __dask_scheduler__ = staticmethod(threaded.get)

    def __dask_postcompute__(self):
        return finalize, ()

    def __dask_postpersist__(self):
        return Array, (self.name, self.chunks, self.dtype)

    @property
    def numblocks(self):
        return tuple(map(len, self.chunks))

    @property
    def npartitions(self):
        return reduce(mul, self.numblocks, 1)

    @property
    def shape(self):
        return tuple(map(sum, self.chunks))

    @property
    def _meta(self):
        return np.empty(shape=(), dtype=self.dtype)

    def _get_chunks(self):
        return self._chunks

    def _set_chunks(self, chunks):
        raise TypeError("Can not set chunks directly\n\n"
                        "Please use the rechunk method instead:\n"
                        "  x.rechunk(%s)" % str(chunks))

    chunks = property(_get_chunks, _set_chunks, "chunks property")

    def __len__(self):
        if not self.chunks:
            raise TypeError("len() of unsized object")
        return sum(self.chunks[0])

    def __array_ufunc__(self, numpy_ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, (np.ndarray, Number, Array)):
                return NotImplemented

        if method == '__call__':
            if numpy_ufunc.signature is not None:
                from .gufunc import apply_gufunc
                return apply_gufunc(numpy_ufunc,
                                    numpy_ufunc.signature,
                                    *inputs,
                                    **kwargs)
            if numpy_ufunc.nout > 1:
                from . import ufunc
                try:
                    da_ufunc = getattr(ufunc, numpy_ufunc.__name__)
                except AttributeError:
                    return NotImplemented
                return da_ufunc(*inputs, **kwargs)
            else:
                return elemwise(numpy_ufunc, *inputs, **kwargs)
        elif method == 'outer':
            from . import ufunc
            try:
                da_ufunc = getattr(ufunc, numpy_ufunc.__name__)
            except AttributeError:
                return NotImplemented
            return da_ufunc.outer(*inputs, **kwargs)
        else:
            return NotImplemented

    def __repr__(self):
        """

        >>> import dask.array as da
        >>> da.ones((10, 10), chunks=(5, 5), dtype='i4')
        dask.array<..., shape=(10, 10), dtype=int32, chunksize=(5, 5)>
        """
        chunksize = str(tuple(c[0] for c in self.chunks))
        name = self.name.rsplit('-', 1)[0]
        return ("dask.array<%s, shape=%s, dtype=%s, chunksize=%s>" %
                (name, self.shape, self.dtype, chunksize))

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def size(self):
        """ Number of elements in array """
        return reduce(mul, self.shape, 1)

    @property
    def nbytes(self):
        """ Number of bytes in array """
        return self.size * self.dtype.itemsize

    @property
    def itemsize(self):
        """ Length of one array element in bytes """
        return self.dtype.itemsize

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val
        # Clear the key cache when the name is reset
        self._cached_keys = None

    __array_priority__ = 11  # higher than numpy.ndarray and numpy.matrix

    def __array__(self, dtype=None, **kwargs):
        x = self.compute()
        if dtype and x.dtype != dtype:
            x = x.astype(dtype)
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        return x

    @property
    def _elemwise(self):
        return elemwise

    @wraps(store)
    def store(self, target, **kwargs):
        r = store([self], [target], **kwargs)

        if kwargs.get("return_stored", False):
            r = r[0]

        return r

    def to_hdf5(self, filename, datapath, **kwargs):
        """ Store array in HDF5 file

        >>> x.to_hdf5('myfile.hdf5', '/x')  # doctest: +SKIP

        Optionally provide arguments as though to ``h5py.File.create_dataset``

        >>> x.to_hdf5('myfile.hdf5', '/x', compression='lzf', shuffle=True)  # doctest: +SKIP

        See Also
        --------
        da.store
        h5py.File.create_dataset
        """
        return to_hdf5(filename, datapath, self, **kwargs)

    def to_dask_dataframe(self, columns=None):
        """ Convert dask Array to dask Dataframe

        Parameters
        ----------
        columns: list or string
            list of column names if DataFrame, single string if Series

        See Also
        --------
        dask.dataframe.from_dask_array
        """
        from ..dataframe import from_dask_array
        return from_dask_array(self, columns=columns)

    def __bool__(self):
        if self.size > 1:
            raise ValueError("The truth value of a {0} is ambiguous. "
                             "Use a.any() or a.all()."
                             .format(self.__class__.__name__))
        else:
            return bool(self.compute())

    __nonzero__ = __bool__  # python 2

    def _scalarfunc(self, cast_type):
        if self.size > 1:
            raise TypeError("Only length-1 arrays can be converted "
                            "to Python scalars")
        else:
            return cast_type(self.compute())

    def __int__(self):
        return self._scalarfunc(int)

    __long__ = __int__  # python 2

    def __float__(self):
        return self._scalarfunc(float)

    def __complex__(self):
        return self._scalarfunc(complex)

    def __setitem__(self, key, value):
        from .routines import where
        if isinstance(key, Array):
            if isinstance(value, Array) and value.ndim > 1:
                raise ValueError('boolean index array should have 1 dimension')
            y = where(key, value, self)
            self.dtype = y.dtype
            self.dask = y.dask
            self.name = y.name
            return self
        else:
            raise NotImplementedError("Item assignment with %s not supported"
                                      % type(key))

    def __getitem__(self, index):
        # Field access, e.g. x['a'] or x[['a', 'b']]
        if (isinstance(index, (str, unicode)) or
                (isinstance(index, list) and index and
                 all(isinstance(i, (str, unicode)) for i in index))):
            if isinstance(index, (str, unicode)):
                dt = self.dtype[index]
            else:
                dt = _make_sliced_dtype(self.dtype, index)

            if dt.shape:
                new_axis = list(range(self.ndim, self.ndim + len(dt.shape)))
                chunks = self.chunks + tuple((i,) for i in dt.shape)
                return self.map_blocks(getitem, index, dtype=dt.base,
                                       chunks=chunks, new_axis=new_axis)
            else:
                return self.map_blocks(getitem, index, dtype=dt)

        if not isinstance(index, tuple):
            index = (index,)

        from .slicing import normalize_index, slice_with_dask_array
        index2 = normalize_index(index, self.shape)

        if any(isinstance(i, Array) for i in index2):
            self, index2 = slice_with_dask_array(self, index2)

        if all(isinstance(i, slice) and i == slice(None) for i in index2):
            return self

        out = 'getitem-' + tokenize(self, index2)
        dsk, chunks = slice_array(out, self.name, self.chunks, index2)

        dsk2 = sharedict.merge(self.dask, (out, dsk))

        return Array(dsk2, out, chunks, dtype=self.dtype)

    def _vindex(self, key):
        if not isinstance(key, tuple):
            key = (key,)
        if any(k is None for k in key):
            raise IndexError(
                "vindex does not support indexing with None (np.newaxis), "
                "got {}".format(key))
        if all(isinstance(k, slice) for k in key):
            if all(k.indices(d) == slice(0, d).indices(d)
                   for k, d in zip(key, self.shape)):
                return self
            raise IndexError(
                "vindex requires at least one non-slice to vectorize over "
                "when the slices are not over the entire array (i.e, x[:]). "
                "Use normal slicing instead when only using slices. Got: {}"
                .format(key))
        return _vindex(self, *key)

    @property
    def vindex(self):
        """Vectorized indexing with broadcasting.

        This is equivalent to numpy's advanced indexing, using arrays that are
        broadcast against each other. This allows for pointwise indexing:

        >>> x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> x = from_array(x, chunks=2)
        >>> x.vindex[[0, 1, 2], [0, 1, 2]].compute()
        array([1, 5, 9])

        Mixed basic/advanced indexing with slices/arrays is also supported. The
        order of dimensions in the result follows those proposed for
        ndarray.vindex [1]_: the subspace spanned by arrays is followed by all
        slices.

        Note: ``vindex`` provides more general functionality than standard
        indexing, but it also has fewer optimizations and can be significantly
        slower.

        _[1]: https://github.com/numpy/numpy/pull/6256
        """
        return IndexCallable(self._vindex)

    @derived_from(np.ndarray)
    def dot(self, other):
        from .routines import tensordot
        return tensordot(self, other,
                         axes=((self.ndim - 1,), (other.ndim - 2,)))

    @property
    def A(self):
        return self

    @property
    def T(self):
        return self.transpose()

    @derived_from(np.ndarray)
    def transpose(self, *axes):
        from .routines import transpose
        if not axes:
            axes = None
        elif len(axes) == 1 and isinstance(axes[0], Iterable):
            axes = axes[0]
        return transpose(self, axes=axes)

    @derived_from(np.ndarray)
    def ravel(self):
        from .routines import ravel
        return ravel(self)

    flatten = ravel

    @derived_from(np.ndarray)
    def choose(self, choices):
        from .routines import choose
        return choose(self, choices)

    @derived_from(np.ndarray)
    def reshape(self, *shape):
        from .reshape import reshape
        if len(shape) == 1 and not isinstance(shape[0], Number):
            shape = shape[0]
        return reshape(self, shape)

    def topk(self, k, axis=-1, split_every=None):
        """The top k elements of an array.

        See ``da.topk`` for docstring"""
        from .reductions import topk
        return topk(self, k, axis=axis, split_every=split_every)

    def argtopk(self, k, axis=-1, split_every=None):
        """The indices of the top k elements of an array.

        See ``da.argtopk`` for docstring"""
        from .reductions import argtopk
        return argtopk(self, k, axis=axis, split_every=split_every)

    def astype(self, dtype, **kwargs):
        """Copy of the array, cast to a specified type.

        Parameters
        ----------
        dtype : str or dtype
            Typecode or data-type to which the array is cast.
        casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
            Controls what kind of data casting may occur. Defaults to 'unsafe'
            for backwards compatibility.

            * 'no' means the data types should not be cast at all.
            * 'equiv' means only byte-order changes are allowed.
            * 'safe' means only casts which can preserve values are allowed.
            * 'same_kind' means only safe casts or casts within a kind,
                like float64 to float32, are allowed.
            * 'unsafe' means any data conversions may be done.
        copy : bool, optional
            By default, astype always returns a newly allocated array. If this
            is set to False and the `dtype` requirement is satisfied, the input
            array is returned instead of a copy.
        """
        # Scalars don't take `casting` or `copy` kwargs - as such we only pass
        # them to `map_blocks` if specified by user (different than defaults).
        extra = set(kwargs) - {'casting', 'copy'}
        if extra:
            raise TypeError("astype does not take the following keyword "
                            "arguments: {0!s}".format(list(extra)))
        casting = kwargs.get('casting', 'unsafe')
        dtype = np.dtype(dtype)
        if self.dtype == dtype:
            return self
        elif not np.can_cast(self.dtype, dtype, casting=casting):
            raise TypeError("Cannot cast array from {0!r} to {1!r}"
                            " according to the rule "
                            "{2!r}".format(self.dtype, dtype, casting))
        return self.map_blocks(chunk.astype, dtype=dtype,
                               astype_dtype=dtype, **kwargs)

    def __abs__(self):
        return elemwise(operator.abs, self)

    def __add__(self, other):
        return elemwise(operator.add, self, other)

    def __radd__(self, other):
        return elemwise(operator.add, other, self)

    def __and__(self, other):
        return elemwise(operator.and_, self, other)

    def __rand__(self, other):
        return elemwise(operator.and_, other, self)

    def __div__(self, other):
        return elemwise(operator.div, self, other)

    def __rdiv__(self, other):
        return elemwise(operator.div, other, self)

    def __eq__(self, other):
        return elemwise(operator.eq, self, other)

    def __gt__(self, other):
        return elemwise(operator.gt, self, other)

    def __ge__(self, other):
        return elemwise(operator.ge, self, other)

    def __invert__(self):
        return elemwise(operator.invert, self)

    def __lshift__(self, other):
        return elemwise(operator.lshift, self, other)

    def __rlshift__(self, other):
        return elemwise(operator.lshift, other, self)

    def __lt__(self, other):
        return elemwise(operator.lt, self, other)

    def __le__(self, other):
        return elemwise(operator.le, self, other)

    def __mod__(self, other):
        return elemwise(operator.mod, self, other)

    def __rmod__(self, other):
        return elemwise(operator.mod, other, self)

    def __mul__(self, other):
        return elemwise(operator.mul, self, other)

    def __rmul__(self, other):
        return elemwise(operator.mul, other, self)

    def __ne__(self, other):
        return elemwise(operator.ne, self, other)

    def __neg__(self):
        return elemwise(operator.neg, self)

    def __or__(self, other):
        return elemwise(operator.or_, self, other)

    def __pos__(self):
        return self

    def __ror__(self, other):
        return elemwise(operator.or_, other, self)

    def __pow__(self, other):
        return elemwise(operator.pow, self, other)

    def __rpow__(self, other):
        return elemwise(operator.pow, other, self)

    def __rshift__(self, other):
        return elemwise(operator.rshift, self, other)

    def __rrshift__(self, other):
        return elemwise(operator.rshift, other, self)

    def __sub__(self, other):
        return elemwise(operator.sub, self, other)

    def __rsub__(self, other):
        return elemwise(operator.sub, other, self)

    def __truediv__(self, other):
        return elemwise(operator.truediv, self, other)

    def __rtruediv__(self, other):
        return elemwise(operator.truediv, other, self)

    def __floordiv__(self, other):
        return elemwise(operator.floordiv, self, other)

    def __rfloordiv__(self, other):
        return elemwise(operator.floordiv, other, self)

    def __xor__(self, other):
        return elemwise(operator.xor, self, other)

    def __rxor__(self, other):
        return elemwise(operator.xor, other, self)

    def __matmul__(self, other):
        from .routines import matmul
        return matmul(self, other)

    def __rmatmul__(self, other):
        from .routines import matmul
        return matmul(other, self)

    @derived_from(np.ndarray)
    def any(self, axis=None, keepdims=False, split_every=None, out=None):
        from .reductions import any
        return any(self, axis=axis, keepdims=keepdims, split_every=split_every,
                   out=out)

    @derived_from(np.ndarray)
    def all(self, axis=None, keepdims=False, split_every=None, out=None):
        from .reductions import all
        return all(self, axis=axis, keepdims=keepdims, split_every=split_every,
                   out=out)

    @derived_from(np.ndarray)
    def min(self, axis=None, keepdims=False, split_every=None, out=None):
        from .reductions import min
        return min(self, axis=axis, keepdims=keepdims, split_every=split_every,
                   out=out)

    @derived_from(np.ndarray)
    def max(self, axis=None, keepdims=False, split_every=None, out=None):
        from .reductions import max
        return max(self, axis=axis, keepdims=keepdims, split_every=split_every,
                   out=out)

    @derived_from(np.ndarray)
    def argmin(self, axis=None, split_every=None, out=None):
        from .reductions import argmin
        return argmin(self, axis=axis, split_every=split_every, out=out)

    @derived_from(np.ndarray)
    def argmax(self, axis=None, split_every=None, out=None):
        from .reductions import argmax
        return argmax(self, axis=axis, split_every=split_every, out=out)

    @derived_from(np.ndarray)
    def sum(self, axis=None, dtype=None, keepdims=False, split_every=None,
            out=None):
        from .reductions import sum
        return sum(self, axis=axis, dtype=dtype, keepdims=keepdims,
                   split_every=split_every, out=out)

    @derived_from(np.ndarray)
    def prod(self, axis=None, dtype=None, keepdims=False, split_every=None,
             out=None):
        from .reductions import prod
        return prod(self, axis=axis, dtype=dtype, keepdims=keepdims,
                    split_every=split_every, out=out)

    @derived_from(np.ndarray)
    def mean(self, axis=None, dtype=None, keepdims=False, split_every=None,
             out=None):
        from .reductions import mean
        return mean(self, axis=axis, dtype=dtype, keepdims=keepdims,
                    split_every=split_every, out=out)

    @derived_from(np.ndarray)
    def std(self, axis=None, dtype=None, keepdims=False, ddof=0,
            split_every=None, out=None):
        from .reductions import std
        return std(self, axis=axis, dtype=dtype, keepdims=keepdims, ddof=ddof,
                   split_every=split_every, out=out)

    @derived_from(np.ndarray)
    def var(self, axis=None, dtype=None, keepdims=False, ddof=0,
            split_every=None, out=None):
        from .reductions import var
        return var(self, axis=axis, dtype=dtype, keepdims=keepdims, ddof=ddof,
                   split_every=split_every, out=out)

    def moment(self, order, axis=None, dtype=None, keepdims=False, ddof=0,
               split_every=None, out=None):
        """Calculate the nth centralized moment.

        Parameters
        ----------
        order : int
            Order of the moment that is returned, must be >= 2.
        axis : int, optional
            Axis along which the central moment is computed. The default is to
            compute the moment of the flattened array.
        dtype : data-type, optional
            Type to use in computing the moment. For arrays of integer type the
            default is float64; for arrays of float types it is the same as the
            array type.
        keepdims : bool, optional
            If this is set to True, the axes which are reduced are left in the
            result as dimensions with size one. With this option, the result
            will broadcast correctly against the original array.
        ddof : int, optional
            "Delta Degrees of Freedom": the divisor used in the calculation is
            N - ddof, where N represents the number of elements. By default
            ddof is zero.

        Returns
        -------
        moment : ndarray

        References
        ----------
        .. [1] Pebay, Philippe (2008), "Formulas for Robust, One-Pass Parallel
        Computation of Covariances and Arbitrary-Order Statistical Moments"
        (PDF), Technical Report SAND2008-6212, Sandia National Laboratories

        """

        from .reductions import moment
        return moment(self, order, axis=axis, dtype=dtype, keepdims=keepdims,
                      ddof=ddof, split_every=split_every, out=out)

    def vnorm(self, ord=None, axis=None, keepdims=False, split_every=None,
              out=None):
        """ Vector norm """
        from .reductions import vnorm
        return vnorm(self, ord=ord, axis=axis, keepdims=keepdims,
                     split_every=split_every, out=out)

    @wraps(map_blocks)
    def map_blocks(self, func, *args, **kwargs):
        return map_blocks(func, self, *args, **kwargs)

    def map_overlap(self, func, depth, boundary=None, trim=True, **kwargs):
        """ Map a function over blocks of the array with some overlap

        We share neighboring zones between blocks of the array, then map a
        function, then trim away the neighboring strips.

        Parameters
        ----------
        func: function
            The function to apply to each extended block
        depth: int, tuple, or dict
            The number of elements that each block should share with its neighbors
            If a tuple or dict then this can be different per axis
        boundary: str, tuple, dict
            How to handle the boundaries.
            Values include 'reflect', 'periodic', 'nearest', 'none',
            or any constant value like 0 or np.nan
        trim: bool
            Whether or not to trim ``depth`` elements from each block after
            calling the map function.
            Set this to False if your mapping function already does this for you
        **kwargs:
            Other keyword arguments valid in ``map_blocks``

        Examples
        --------
        >>> x = np.array([1, 1, 2, 3, 3, 3, 2, 1, 1])
        >>> x = from_array(x, chunks=5)
        >>> def derivative(x):
        ...     return x - np.roll(x, 1)

        >>> y = x.map_overlap(derivative, depth=1, boundary=0)
        >>> y.compute()
        array([ 1,  0,  1,  1,  0,  0, -1, -1,  0])

        >>> import dask.array as da
        >>> x = np.arange(16).reshape((4, 4))
        >>> d = da.from_array(x, chunks=(2, 2))
        >>> d.map_overlap(lambda x: x + x.size, depth=1).compute()
        array([[16, 17, 18, 19],
               [20, 21, 22, 23],
               [24, 25, 26, 27],
               [28, 29, 30, 31]])

        >>> func = lambda x: x + x.size
        >>> depth = {0: 1, 1: 1}
        >>> boundary = {0: 'reflect', 1: 'none'}
        >>> d.map_overlap(func, depth, boundary).compute()  # doctest: +NORMALIZE_WHITESPACE
        array([[12,  13,  14,  15],
               [16,  17,  18,  19],
               [20,  21,  22,  23],
               [24,  25,  26,  27]])
        """
        from .ghost import map_overlap
        return map_overlap(self, func, depth, boundary, trim, **kwargs)

    def cumsum(self, axis, dtype=None, out=None):
        """ See da.cumsum for docstring """
        from .reductions import cumsum
        return cumsum(self, axis, dtype, out=out)

    def cumprod(self, axis, dtype=None, out=None):
        """ See da.cumprod for docstring """
        from .reductions import cumprod
        return cumprod(self, axis, dtype, out=out)

    @derived_from(np.ndarray)
    def squeeze(self, axis=None):
        from .routines import squeeze
        return squeeze(self, axis)

    def rechunk(self, chunks, threshold=None, block_size_limit=None):
        """ See da.rechunk for docstring """
        from . import rechunk   # avoid circular import
        return rechunk(self, chunks, threshold, block_size_limit)

    @property
    def real(self):
        from .ufunc import real
        return real(self)

    @property
    def imag(self):
        from .ufunc import imag
        return imag(self)

    def conj(self):
        from .ufunc import conj
        return conj(self)

    @derived_from(np.ndarray)
    def clip(self, min=None, max=None):
        from .ufunc import clip
        return clip(self, min, max)

    def view(self, dtype, order='C'):
        """ Get a view of the array as a new data type

        Parameters
        ----------
        dtype:
            The dtype by which to view the array
        order: string
            'C' or 'F' (Fortran) ordering

        This reinterprets the bytes of the array under a new dtype.  If that
        dtype does not have the same size as the original array then the shape
        will change.

        Beware that both numpy and dask.array can behave oddly when taking
        shape-changing views of arrays under Fortran ordering.  Under some
        versions of NumPy this function will fail when taking shape-changing
        views of Fortran ordered arrays if the first dimension has chunks of
        size one.
        """
        dtype = np.dtype(dtype)
        mult = self.dtype.itemsize / dtype.itemsize

        if order == 'C':
            chunks = self.chunks[:-1] + (tuple(ensure_int(c * mult)
                                         for c in self.chunks[-1]),)
        elif order == 'F':
            chunks = ((tuple(ensure_int(c * mult) for c in self.chunks[0]), ) +
                      self.chunks[1:])
        else:
            raise ValueError("Order must be one of 'C' or 'F'")

        return self.map_blocks(chunk.view, dtype, order=order,
                               dtype=dtype, chunks=chunks)

    @derived_from(np.ndarray)
    def swapaxes(self, axis1, axis2):
        from .routines import swapaxes
        return swapaxes(self, axis1, axis2)

    @derived_from(np.ndarray)
    def round(self, decimals=0):
        from .routines import round
        return round(self, decimals=decimals)

    def copy(self):
        """
        Copy array.  This is a no-op for dask.arrays, which are immutable
        """
        return Array(self.dask, self.name, self.chunks, self.dtype)

    def __deepcopy__(self, memo):
        c = self.copy()
        memo[id(self)] = c
        return c

    def to_delayed(self, optimize_graph=True):
        """Convert into an array of ``dask.delayed`` objects, one per chunk.

        Parameters
        ----------
        optimize_graph : bool, optional
            If True [default], the graph is optimized before converting into
            ``dask.delayed`` objects.

        See Also
        --------
        dask.array.from_delayed
        """
        from ..delayed import Delayed
        keys = self.__dask_keys__()
        dsk = self.__dask_graph__()
        if optimize_graph:
            dsk = self.__dask_optimize__(dsk, keys)
        L = ndeepmap(self.ndim, lambda k: Delayed(k, dsk), keys)
        return np.array(L, dtype=object)

    @derived_from(np.ndarray)
    def repeat(self, repeats, axis=None):
        from .creation import repeat
        return repeat(self, repeats, axis=axis)

    @derived_from(np.ndarray)
    def nonzero(self):
        from .routines import nonzero
        return nonzero(self)

    def to_zarr(self, *args, **kwargs):
        """Save array to the zarr storage format

        See https://zarr.readthedocs.io for details about the format.

        See function ``to_zarr()`` for parameters.
        """
        return to_zarr(self, *args, **kwargs)
