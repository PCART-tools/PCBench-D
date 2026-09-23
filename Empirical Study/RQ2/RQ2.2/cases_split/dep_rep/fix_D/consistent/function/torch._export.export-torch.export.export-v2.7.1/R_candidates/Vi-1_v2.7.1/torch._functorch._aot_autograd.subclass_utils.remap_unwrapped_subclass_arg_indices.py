def remap_unwrapped_subclass_arg_indices(wrapped_args, static_input_indices):
    static_input_indices = set(static_input_indices)
    new_ind = 0
    remapped_static_indices = []
    for i, arg in enumerate(wrapped_args):
        num_indices = 1
        if is_traceable_wrapper_subclass(arg):
            num_indices = (
                len(get_plain_tensors(typing.cast(Tensor, arg), out=[]))
                + len(filter_symints(arg.size()))
                + len(filter_symints(arg.stride()))
            )

        for _ in range(num_indices):
            if i in static_input_indices:
                remapped_static_indices.append(new_ind)

            new_ind += 1

    return remapped_static_indices
