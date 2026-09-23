    @zeros_and_scatter.register_vmap  # type: ignore[misc]
    def _(info, indims, shape, indices, value):  # type: ignore[no-untyped-def]
        """The batching rule is special in that it returns a tensor that is not batched"""
        indices_indims = indims[1]
        expanded_indices = []
        for idx, idx_indim in zip(indices, indices_indims):
            # The index is not a being batched, we should unsqueeze and expand to val
            if idx_indim is None:
                expanded_indices.append(idx.expand(value.shape))
            else:
                # the index is being part of the vmap batch, it should be the same size as val
                assert idx.shape == value.shape
                expanded_indices.append(idx)

        out = torch.ops.flex_lib.zeros_and_scatter(
            shape,
            expanded_indices,
            value,
        )
        return out, None
