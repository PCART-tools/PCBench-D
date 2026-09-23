def prepare_inputs(bsr, *dense_tensors):
    # Introduce fake batch dimension if not present for convenience.
    crow_indices = bsr.crow_indices().unsqueeze(0)
    col_indices = bsr.col_indices().unsqueeze(0)
    values = make_triton_contiguous(bsr.values().unsqueeze(0))
    tensors = [make_triton_contiguous(t.unsqueeze(0)) for t in dense_tensors]

    # Compute broadcasted batch dimension
    batch_dims_broadcasted = torch.broadcast_shapes(
        values.shape[:-3], *(t.shape[:-2] for t in tensors)
    )

    # Broadcast batch dimensions and squash.
    # The result can be either a view or a copy.
    def batch_broadcast_and_squash(t, batch_dims, invariant_dims):
        return t.broadcast_to(batch_dims + invariant_dims).flatten(
            0, len(batch_dims) - 1
        )

    crow_indices = batch_broadcast_and_squash(
        crow_indices, batch_dims_broadcasted, (-1,)
    )

    col_indices = batch_broadcast_and_squash(col_indices, batch_dims_broadcasted, (-1,))
    values = batch_broadcast_and_squash(
        values, batch_dims_broadcasted, values.shape[-3:]
    )
    tensors = [
        batch_broadcast_and_squash(t, batch_dims_broadcasted, t.shape[-2:])
        for t in tensors
    ]

    return crow_indices, col_indices, values, *tensors
