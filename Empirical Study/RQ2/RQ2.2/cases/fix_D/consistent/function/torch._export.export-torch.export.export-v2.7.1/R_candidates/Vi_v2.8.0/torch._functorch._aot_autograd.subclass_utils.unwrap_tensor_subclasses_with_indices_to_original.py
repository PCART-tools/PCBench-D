def unwrap_tensor_subclasses_with_indices_to_original(wrapped_args):
    ret_unwrapped = []
    ret_indices_to_original = []
    for i, a in enumerate(wrapped_args):
        a_unwrapped = unwrap_tensor_subclasses([a], append_symints=False)
        ret_unwrapped.extend(a_unwrapped)
        n = len(a_unwrapped)
        ret_indices_to_original.extend([i] * n)

    return ret_unwrapped, ret_indices_to_original
