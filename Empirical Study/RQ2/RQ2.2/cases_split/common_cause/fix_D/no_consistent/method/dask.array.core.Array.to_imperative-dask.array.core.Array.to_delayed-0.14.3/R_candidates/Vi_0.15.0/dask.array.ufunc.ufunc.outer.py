    @copy_docstring(source=np.ufunc.outer)
    def outer(self, A, B, **kwargs):
        if self.nin != 2:
            raise ValueError("outer product only supported for binary functions")
        if 'out' in kwargs:
            raise ValueError("`out` kwarg not supported")

        A_is_dask = isinstance(A, Base)
        B_is_dask = isinstance(B, Base)
        if not A_is_dask and not B_is_dask:
            return self._ufunc.outer(A, B, **kwargs)
        elif (A_is_dask and not isinstance(A, Array) or
              B_is_dask and not isinstance(B, Array)):
            raise NotImplementedError("Dask objects besides `dask.array.Array` "
                                      "are not supported at this time.")

        A = asarray(A)
        B = asarray(B)
        ndim = A.ndim + B.ndim
        out_inds = tuple(range(ndim))
        A_inds = out_inds[:A.ndim]
        B_inds = out_inds[A.ndim:]

        dtype = apply_infer_dtype(self._ufunc.outer, [A, B], kwargs,
                                  'ufunc.outer', suggest_dtype=False)

        if 'dtype' in kwargs:
            func = partial(self._ufunc.outer, dtype=kwargs.pop('dtype'))
        else:
            func = self._ufunc.outer

        return atop(func, out_inds, A, A_inds, B, B_inds, dtype=dtype,
                    token=self.__name__ + '.outer', **kwargs)
