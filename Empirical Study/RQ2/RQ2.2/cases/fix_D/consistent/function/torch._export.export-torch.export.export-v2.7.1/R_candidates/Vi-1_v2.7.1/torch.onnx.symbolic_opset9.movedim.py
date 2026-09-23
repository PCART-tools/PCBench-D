@_onnx_symbolic("aten::movedim")
@symbolic_helper.parse_args("v", "t", "t")
def movedim(g: jit_utils.GraphContext, self, source, destination):
    # This is a pythonic implementation mostly taken from aten/src/ATen/native/TensorShape.cpp::movedim
    source = source.view(-1)
    destination = destination.view(-1)

    assert source.size() == destination.size()

    if (source == destination).all():
        return self

    self_rank = symbolic_helper._get_tensor_rank(self)
    assert self_rank is not None

    perm = list(range(self_rank))

    src_dims = perm.copy()
    dst_dims = perm.copy()

    for src, dst in zip(source.tolist(), destination.tolist()):
        perm[dst] = src
        src_dims[src] = -1
        dst_dims[dst] = -1

    src_dims = [dim for dim in src_dims if dim != -1]
    dst_dims = [dim for dim in dst_dims if dim != -1]

    for src, dst in zip(src_dims, dst_dims):
        perm[dst] = src

    return g.op("Transpose", self, perm_i=perm)
