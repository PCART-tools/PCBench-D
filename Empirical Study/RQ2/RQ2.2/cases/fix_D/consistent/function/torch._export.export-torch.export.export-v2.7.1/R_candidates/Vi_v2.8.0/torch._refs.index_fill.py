@register_decomposition(aten.index_fill)
@out_wrapper()
def index_fill(
    x: TensorLike, dim: int, index: TensorLike, value: Union[NumberType, TensorLike]
):
    return _index_fill(x, dim, index, value, inplace=False)
