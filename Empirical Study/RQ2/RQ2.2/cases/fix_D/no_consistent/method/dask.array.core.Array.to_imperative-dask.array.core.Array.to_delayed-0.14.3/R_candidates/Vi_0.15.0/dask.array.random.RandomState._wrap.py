    def _wrap(self, func, *args, **kwargs):
        """ Wrap numpy random function to produce dask.array random function

        extra_chunks should be a chunks tuple to append to the end of chunks
        """
        size = kwargs.pop('size', None)
        chunks = kwargs.pop('chunks')
        extra_chunks = kwargs.pop('extra_chunks', ())

        if size is not None and not isinstance(size, (tuple, list)):
            size = (size,)

        args_shapes = {ar.shape for ar in args
                       if isinstance(ar, (Array, np.ndarray))}
        args_shapes.union({ar.shape for ar in kwargs.values()
                           if isinstance(ar, (Array, np.ndarray))})

        shapes = list(args_shapes)
        if size is not None:
            shapes += [size]
        # broadcast to the final size(shape)
        size = broadcast_shapes(*shapes)
        chunks = normalize_chunks(chunks, size)
        slices = slices_from_chunks(chunks)

        def _broadcast_any(ar, shape, chunks):
            if isinstance(ar, Array):
                return broadcast_to(ar, shape).rechunk(chunks)
            if isinstance(ar, np.ndarray):
                return np.ascontiguousarray(np.broadcast_to(ar, shape))

        # Broadcast all arguments, get tiny versions as well
        # Start adding the relevant bits to the graph
        dsk = {}
        dsks = []
        lookup = {}
        small_args = []
        for i, ar in enumerate(args):
            if isinstance(ar, (np.ndarray, Array)):
                res = _broadcast_any(ar, size, chunks)
                if isinstance(res, Array):
                    dsks.append(res.dask)
                    lookup[i] = res.name
                elif isinstance(res, np.ndarray):
                    name = 'array-{}'.format(tokenize(res))
                    lookup[i] = name
                    dsk[name] = res
                small_args.append(ar[tuple(0 for _ in ar.shape)])
            else:
                small_args.append(ar)

        small_kwargs = {}
        for key, ar in kwargs.items():
            if isinstance(ar, (np.ndarray, Array)):
                res = _broadcast_any(ar, size, chunks)
                if isinstance(res, Array):
                    dsks.append(res.dask)
                    lookup[key] = res.name
                elif isinstance(res, np.ndarray):
                    name = 'array-{}'.format(tokenize(res))
                    lookup[key] = name
                    dsk[name] = res
                small_kwargs[key] = ar[tuple(0 for _ in ar.shape)]
            else:
                small_kwargs[key] = ar

        # Get dtype
        small_kwargs['size'] = (0,)
        dtype = func(np.random.RandomState(), *small_args,
                     **small_kwargs).dtype

        sizes = list(product(*chunks))
        state_data = random_state_data(len(sizes), self._numpy_state)
        token = tokenize(state_data, size, chunks, args, kwargs)
        name = 'da.random.{0}-{1}'.format(func.__name__, token)

        keys = product([name], *([range(len(bd)) for bd in chunks] +
                                 [[0]] * len(extra_chunks)))
        blocks = product(*[range(len(bd)) for bd in chunks])
        vals = []
        for state, size, slc, block in zip(state_data, sizes, slices, blocks):
            arg = []
            for i, ar in enumerate(args):
                if i not in lookup:
                    arg.append(ar)
                else:
                    if isinstance(ar, Array):
                        arg.append((lookup[i], ) + block)
                    else:   # np.ndarray
                        arg.append((getitem, lookup[i], slc))
            kwrg = {}
            for k, ar in kwargs.items():
                if k not in lookup:
                    kwrg[k] = ar
                else:
                    if isinstance(ar, Array):
                        kwrg[k] = (lookup[k], ) + block
                    else:   # np.ndarray
                        kwrg[k] = (getitem, lookup[k], slc)
            vals.append((_apply_random, func.__name__, state, size, arg, kwrg))
        dsk.update(dict(zip(keys, vals)))
        dsk = sharedict.merge((name, dsk), *dsks)
        return Array(dsk, name, chunks + extra_chunks, dtype=dtype)
