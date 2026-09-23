def dim_movedim(
    ndim: int,
    input: DimsType,
    destination: DimsType,
) -> DimMap:
    input = normalize_dims(input, ndim)
    destination = normalize_dims(destination, ndim)

    assert len(input) == len(destination)
    input_set = set(input)
    assert len(input_set) == len(input), "Found repeated input dims"
    assert len(set(destination)) == len(destination), "Found repeated output dims"
    assert max(input) < ndim
    assert max(destination) < ndim

    dest = [-1] * ndim
    for i, d in zip(input, destination):
        dest[d] = i

    unused_inputs_iter = iter(i for i in range(ndim) if i not in input_set)
    for i in range(ndim):
        if dest[i] == -1:
            dest[i] = next(unused_inputs_iter)

    return tuple(InputDim(i) for i in dest)
