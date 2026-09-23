def make_block(values, placement, klass=None, ndim=None,
               dtype=None, fastpath=False):
    if klass is None:
        dtype = dtype or values.dtype
        vtype = dtype.type

        if isinstance(values, SparseArray):
            klass = SparseBlock
        elif issubclass(vtype, np.floating):
            klass = FloatBlock
        elif (issubclass(vtype, np.integer) and
                issubclass(vtype, np.timedelta64)):
            klass = TimeDeltaBlock
        elif (issubclass(vtype, np.integer) and
                not issubclass(vtype, np.datetime64)):
            klass = IntBlock
        elif dtype == np.bool_:
            klass = BoolBlock
        elif issubclass(vtype, np.datetime64):
            klass = DatetimeBlock
        elif issubclass(vtype, np.complexfloating):
            klass = ComplexBlock
        elif is_categorical(values):
            klass = CategoricalBlock
        else:
            klass = ObjectBlock

    return klass(values, ndim=ndim, fastpath=fastpath,
                 placement=placement)
