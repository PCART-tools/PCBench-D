@register_lowering(aten.split, type_promotion_kind=None)
def split(x, sizes, dim=0):
    dim = _validate_dim(x, dim, 0)
    sizes_ = sizes

    # If sizes is an integer (or a SymInt), we turn it into a list of sizes
    # by computing what the actual size of each chunk should be.
    if not isinstance(sizes, (list, tuple)):
        x_size = x.get_size()[dim]
        chunks = V.graph.sizevars.evaluate_static_shape(
            FloorDiv(x_size + sizes - 1, sizes)
        )
        sizes_ = [sizes] * chunks
        # The last chunk might have a smaller size than the rest.
        sizes_[-1] = x_size - (chunks - 1) * sizes

    # From this point, we assume that the sum of the sizes of all chunks
    # equals the size of the base tensor.
    result = []
    start = 0
    for size in sizes_:
        end = start + size
        # No need for clamping here, since we compute the exact
        # start and end values.
        result.append(slice_(x, dim, start, end, clamp=False))
        start = end
    return result
