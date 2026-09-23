@register_decomposition(aten.index_fill_)
def index_fill_(
    x: TensorLike, dim: int, index: TensorLike, value: Union[NumberType, TensorLike]
):
    return _index_fill(x, dim, index, value, inplace=True)
