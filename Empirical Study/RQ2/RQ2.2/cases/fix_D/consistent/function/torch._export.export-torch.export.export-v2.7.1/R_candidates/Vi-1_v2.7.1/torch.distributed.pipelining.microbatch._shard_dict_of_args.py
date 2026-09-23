def _shard_dict_of_args(
    args_dict,
    args_chunk_spec,
    num_chunks,
):
    """
    Given a dictionary of args, and a dictionary of chunking specs, shard the
    args according to the chunking specs.

    Args:
        args_dict: Dictionary of args
        args_chunk_spec: Dictionary of chunking specs
        num_chunks: Number of chunks to shard the args into

    Returns:
        args_split: List of sharded args
    """
    # Stage 1+2: flatten and shard/replicate

    # args_sharded_replicated : [num args, num flat values, num chunks]
    args_sharded_replicated = {}
    arg_specs = []

    real_num_chunks = num_chunks
    first_tensor = True

    assert len(args_dict) == len(args_chunk_spec), (
        f"args_dict.keys() = {list(args_dict.keys())} args_chunk_spec.keys() = {list(args_chunk_spec.keys())}"
    )

    for arg_key, arg in args_dict.items():
        flat, spec = tree_flatten(arg)
        arg_specs.append(spec)

        chunk_spec = args_chunk_spec[arg_key]
        assert chunk_spec is not None  # Should have been set by caller
        chunk_spec_flat, _ = tree_flatten(chunk_spec)
        if len(flat) != len(chunk_spec_flat):
            raise ValueError(
                f"Argument value {arg} did not have the same number of "
                f"values as as chunk spec {chunk_spec}"
            )

        sharded_arg_flat = []

        for v, chunk_v in zip(flat, chunk_spec_flat):
            if chunk_v is _Replicate or not isinstance(v, torch.Tensor):
                sharded_arg_flat.append([v] * real_num_chunks)
            elif isinstance(chunk_v, TensorChunkSpec):
                # TODO: check type of v. If it's a tensor, use chunk (or debug mask).
                # If it's a collection type, split it as you would expect. Otherwise,
                # Throw an error
                assert isinstance(v, torch.Tensor), f"{v} is not a tensor"

                v_split_dim_size = v.size(chunk_v.split_dim)
                if v_split_dim_size < real_num_chunks:
                    if first_tensor:
                        # We can only adjust number of chunks when we hit this
                        # issue at the first tensor encountered
                        logger.warning(
                            f"Tensor size on chunking dimension is {v_split_dim_size}, "  # noqa: G004
                            f"downsizing the number of chunks from {num_chunks} to {v_split_dim_size}."
                        )
                        real_num_chunks = v_split_dim_size
                    else:
                        raise RuntimeError(
                            f"Arg {arg_key} on chunking dimension has a size of {v_split_dim_size}, "
                            f"smaller than the number of chunks {num_chunks}. "
                            "PiPPy cannot reduce the number of chunks because "
                            "other arguments have bigger chunk-dimension sizes. "
                            "Please adjust your num_chunks setting."
                        )

                chunk_tensors = torch.tensor_split(
                    v, real_num_chunks, chunk_v.split_dim
                )

                if _debug_mask_minibatches:
                    expanded_chunks = []

                    split_dim_idx = 0
                    for chunk_tensor in chunk_tensors:
                        new_val = torch.zeros_like(v)
                        upper_idx = split_dim_idx + chunk_tensor.size(chunk_v.split_dim)

                        slice_indices = [slice(None, None, None)] * new_val.ndim
                        slice_indices[chunk_v.split_dim] = slice(
                            split_dim_idx, upper_idx
                        )
                        new_val[slice_indices] = chunk_tensor

                        expanded_chunks.append(new_val)

                        split_dim_idx += chunk_tensor.size(chunk_v.split_dim)

                    sharded_arg_flat.append(expanded_chunks)
                else:
                    sharded_arg_flat.append(chunk_tensors)  # type: ignore[arg-type]

                first_tensor = False
            else:
                raise TypeError(f"Unrecognized chunk spec: {chunk_v}")

        args_sharded_replicated[arg_key] = sharded_arg_flat

    # chunks_flat : [num chunks, num args, num flat values]
    chunks_flat = []
    for chunk_idx in range(real_num_chunks):
        chunk_args = {}
        for key, arg in args_sharded_replicated.items():
            arg_single_chunk = [v_flat[chunk_idx] for v_flat in arg]
            chunk_args[key] = arg_single_chunk
        chunks_flat.append(chunk_args)

    # args_split : [num chunks, num args]
    args_split = []

    for chunk in chunks_flat:
        per_chunk_args = {}
        assert len(arg_specs) == len(chunk)
        for (key, arg), arg_spec in zip(chunk.items(), arg_specs):
            per_chunk_args[key] = tree_unflatten(arg, arg_spec)
        args_split.append(per_chunk_args)

    return args_split
