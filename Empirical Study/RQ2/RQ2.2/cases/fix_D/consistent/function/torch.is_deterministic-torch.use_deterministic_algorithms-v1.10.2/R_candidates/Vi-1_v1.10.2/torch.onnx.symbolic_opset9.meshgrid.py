@parse_args('v', 's')
def meshgrid(g, tensor_list, indexing: Optional[str] = None):
    if indexing is None:
        indexing = 'ij'
    elif indexing not in {'ij', 'xy'}:
        raise ValueError(f'Unsupported indexing: {indexing}')
    if indexing == 'xy':
        tensor_list[0], tensor_list[1] = tensor_list[1], tensor_list[0]
    tensors = [sym_help._reshape_helper(g, t, g.op("Constant", value_t=torch.LongTensor([-1])))
               for t in sym_help._unpack_list(tensor_list)]
    tensors_shape = [g.op("Shape", t) for t in tensors]
    out_shape = g.op("Concat", *tensors_shape, axis_i=0)
    out = []
    for i, t in enumerate(tensors):
        shape_i = [g.op("Constant", value_t=torch.ones(1, dtype=torch.int64))] * len(tensors)
        shape_i[i] = tensors_shape[i]
        t_reshaped = _reshape_from_tensor(g, t, g.op("Concat", *shape_i, axis_i=0))
        out.append(g.op("Expand", t_reshaped, out_shape))
    if indexing == 'xy':
        out[0], out[1] = out[1], out[0]
    return g.op("prim::ListConstruct", *out)
