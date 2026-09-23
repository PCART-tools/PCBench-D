def _concat_chunked_outputs(out_dims, arg_spec, flat_output_chunks):
    # concat chunks on out_dim
    flat_out_dims = _broadcast_to_and_flatten(out_dims, arg_spec)
    assert len(flat_out_dims) == len(flat_output_chunks)
    flat_output = []
    for idx, out_dim in enumerate(flat_out_dims):
        flat_output.append(torch.cat(flat_output_chunks[idx], dim=out_dim))
        # release tensors
        flat_output_chunks[idx] = None

    return flat_output
