def generate_tensors_from_vals(vals, device, dtype, domain):
    offset = 63

    assert _large_size[1] > (_medium_length + offset)  # large tensor should be large enough
    assert len(vals) < _medium_length  # medium tensor should contain all vals
    assert _medium_length % 4 == 0  # ensure vectorized code coverage

    if not dtype.is_complex:
        # Filter values based on Operators domain.
        # Note: Complex numbers don't belong to ordered field,
        #       so we don't filter for them.
        if domain[0] is not None:
            vals = list(filter(lambda x: x >= domain[0], vals))
        if domain[1] is not None:
            vals = list(filter(lambda x: x < domain[1], vals))

    # Constructs the large tensor containing vals
    large_tensor = make_tensor(_large_size, device=device, dtype=dtype, low=domain[0], high=domain[1])

    # Inserts the vals at an odd place
    large_tensor[57][offset:offset + len(vals)] = torch.tensor(vals, device=device, dtype=dtype)

    # Takes a medium sized copy of the large tensor containing vals
    medium_tensor = large_tensor[57][offset:offset + _medium_length]

    # Constructs scalar tensors
    scalar_tensors = (t.squeeze() for t in torch.split(medium_tensor, 1))

    # Tensors with no elements
    empty_sizes = ((0,), (0, 3, 3), (1, 0, 5), (6, 0, 0, 0), (3, 0, 1, 0))
    empty_tensors = (torch.empty(size, device=device, dtype=dtype) for size in empty_sizes)

    return chain(empty_tensors, scalar_tensors, (medium_tensor,), (large_tensor,))
