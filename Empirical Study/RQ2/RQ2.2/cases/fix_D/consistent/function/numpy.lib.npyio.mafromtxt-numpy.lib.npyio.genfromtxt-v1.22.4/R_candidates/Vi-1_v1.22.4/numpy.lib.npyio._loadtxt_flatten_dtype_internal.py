def _loadtxt_flatten_dtype_internal(dt):
    """Unpack a structured data-type, and produce a packer function."""
    if dt.names is None:
        # If the dtype is flattened, return.
        # If the dtype has a shape, the dtype occurs
        # in the list more than once.
        shape = dt.shape
        if len(shape) == 0:
            return ([dt.base], None)
        else:
            packing = [(shape[-1], list)]
            if len(shape) > 1:
                for dim in dt.shape[-2::-1]:
                    packing = [(dim*packing[0][0], packing*dim)]
            return ([dt.base] * int(np.prod(dt.shape)),
                    functools.partial(_loadtxt_pack_items, packing))
    else:
        types = []
        packing = []
        for field in dt.names:
            tp, bytes = dt.fields[field]
            flat_dt, flat_packer = _loadtxt_flatten_dtype_internal(tp)
            types.extend(flat_dt)
            flat_packing = flat_packer.args[0] if flat_packer else None
            # Avoid extra nesting for subarrays
            if tp.ndim > 0:
                packing.extend(flat_packing)
            else:
                packing.append((len(flat_dt), flat_packing))
        return (types, functools.partial(_loadtxt_pack_items, packing))
