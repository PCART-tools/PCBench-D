def inferUnsqueezeGeometry(tensor, dim):
    result_sizes = list(tensor.size())
    result_strides = list(tensor.stride())
    new_stride = 1 if dim >= tensor.dim() else result_sizes[dim] * result_strides[dim]
    result_sizes.insert(dim, 1)
    result_strides.insert(dim, new_stride)
    return result_sizes, result_strides
